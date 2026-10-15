"""HA admin helper: Unix socket only; accessed through authenticated SSH.

No generic shell/API tool. Deployments use optimistic hashes, on-host backups,
atomic per-file replacement, a durable journal, validation, and explicit reloads.
"""
import base64
import difflib
import hashlib
import http.server
import json
import os
from pathlib import Path, PurePosixPath
import re
import socketserver
import tempfile
import time
import urllib.error
import urllib.request
import uuid

CONFIG = Path('/config')
DATA = Path('/data/deployments')
SOCKET = '/share/codex-ha-admin.sock'
MAX_BODY = 8 * 1024 * 1024
ROOT_FILES = {'configuration.yaml', 'automations.yaml', 'scripts.yaml', 'scenes.yaml',
              'sensors.yaml', 'templates.yaml', 'lights.yaml', 'command_line.yaml',
              'shell_commands.yaml', 'groups.yaml', 'customize.yaml'}
RELOADS = {'automation', 'script', 'template', 'scene', 'group'}


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def redact(value):
    """Best-effort output hygiene, not a substitute for reviewing private data."""
    if isinstance(value, dict):
        return {k: '[redacted]' if re.search(r'password|token|secret|api_key|authorization', k, re.I)
                else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        value = re.sub(r'(?i)(Bearer\s+)[\w.\-]+', r'\1[redacted]', value)
        value = re.sub(r'eyJ[\w-]+\.[\w-]+\.[\w-]+', '[redacted JWT]', value)
        value = re.sub(r'(?im)^(\s*(?:password|token|access_token|api_key|secret)\s*:\s*).+$',
                       r'\1[redacted]', value)
    return value


def api(path, method='GET', body=None, timeout=45, text=False):
    req = urllib.request.Request('http://supervisor/' + path,
        data=None if body is None else json.dumps(body).encode(), method=method,
        headers={'Authorization': 'Bearer ' + os.environ['SUPERVISOR_TOKEN'],
                 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(MAX_BODY + 1)
    except urllib.error.HTTPError as exc:
        raise ValueError('HA API request failed: HTTP ' + str(exc.code)) from None
    if len(raw) > MAX_BODY:
        raise ValueError('HA response exceeds output limit; narrow the request')
    if text:
        return raw.decode('utf-8', errors='replace')
    result = json.loads(raw)
    if isinstance(result, dict) and result.get('result') == 'error':
        raise ValueError(str(redact(result.get('message', 'HA API error'))))
    return result


def websocket_command(message):
    import websocket
    ws = websocket.create_connection('ws://supervisor/core/websocket', timeout=30,
                                      suppress_origin=True)
    try:
        hello = json.loads(ws.recv())
        if hello.get('type') != 'auth_required':
            raise ValueError('Unexpected WebSocket handshake')
        ws.send(json.dumps({'type': 'auth', 'access_token': os.environ['SUPERVISOR_TOKEN']}))
        if json.loads(ws.recv()).get('type') != 'auth_ok':
            raise ValueError('Core WebSocket authentication failed')
        ws.send(json.dumps(dict(message, id=1)))
        for _ in range(10):
            raw = ws.recv()
            if len(raw) > MAX_BODY:
                raise ValueError('Trace is too large')
            result = json.loads(raw)
            if result.get('id') == 1:
                if not result.get('success'):
                    raise ValueError(str(redact(result.get('error'))))
                return result.get('result')
        raise ValueError('No matching WebSocket response')
    finally:
        ws.close()


def safe_path(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Invalid config path')
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ('..', '.') or x.startswith('.') for x in p.parts):
        raise ValueError('Hidden paths and traversal are forbidden')
    allowed = name in ROOT_FILES or (len(p.parts) >= 2 and
        ((p.parts[0] in {'automations', 'dashboards', 'themes', 'packages', 'helpers'} and p.suffix == '.yaml')
         or (p.parts[0] == 'www' and p.suffix in {'.js', '.css'})))
    if not allowed or 'secret' in name.lower():
        raise ValueError('Path is not in the configuration allowlist')
    current = CONFIG
    for part in p.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlink paths are forbidden')
    if current.exists() and not current.is_file():
        raise ValueError('Config path is not a regular file')
    return current


def read_bytes(path):
    if not path.exists():
        return None
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError('File exceeds 2 MiB limit')
    return path.read_bytes()


def atomic_write(path, content, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.codex-stage-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            os.fchmod(f.fileno(), mode)
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def save_plan(plan):
    atomic_write(DATA / plan['id'] / 'manifest.json', json.dumps(plan).encode(), 0o600)


def get_plan(plan_id):
    if not re.fullmatch(r'[a-f0-9]{32}', plan_id):
        raise ValueError('Invalid deployment ID')
    return json.loads((DATA / plan_id / 'manifest.json').read_text())


def config_check():
    return api('core/check', 'POST', {}, timeout=180)


def reload_domains(domains):
    if not isinstance(domains, list) or len(domains) != len(set(domains)) or not set(domains) <= RELOADS:
        raise ValueError('Unsupported reload domain')
    results = {}
    for domain in domains:
        try:
            api('core/api/services/' + domain + '/reload', 'POST', {}, timeout=90)
            results[domain] = 'completed'
        except Exception as exc:
            results[domain] = 'uncertain: ' + str(exc)
    return results


def pending_recovery():
    if not DATA.exists():
        return []
    return [p.parent.name for p in DATA.glob('*/manifest.json')
            if json.loads(p.read_text()).get('status') in {'applying', 'rolling_back', 'recovery_required'}]


def prepare(files):
    import yaml
    if not isinstance(files, list) or not 1 <= len(files) <= 20:
        raise ValueError('Specify 1–20 files')
    if pending_recovery():
        raise ValueError('An interrupted deployment requires recovery before another write')
    plan = {'id': uuid.uuid4().hex, 'created': time.time(), 'status': 'prepared', 'files': []}
    seen = set()
    previews = []
    for item in files:
        name = item['path']
        if name in seen:
            raise ValueError('Duplicate file path')
        seen.add(name)
        path = safe_path(name)
        before = read_bytes(path)
        expected = item['expected_sha256']
        if digest(before) != expected:
            raise ValueError('Live file changed: ' + name)
        after = item['content'].encode('utf-8')
        if not after or len(after) > 2 * 1024 * 1024:
            raise ValueError('File empty or too large')
        if name.endswith('.yaml'):
            # Parsing supports HA tags without executing constructors or includes.
            list(yaml.parse(after))
        entry = {'path': name, 'before_sha256': digest(before), 'after_sha256': digest(after),
                 'mode': (path.stat().st_mode & 0o777) if path.exists() else 0o644,
                 'before': None if before is None else base64.b64encode(before).decode(),
                 'after': base64.b64encode(after).decode()}
        plan['files'].append(entry)
        diff = ''.join(difflib.unified_diff((before or b'').decode().splitlines(True),
                     after.decode().splitlines(True), fromfile='live/' + name, tofile='proposed/' + name))
        previews.append({'path': name, 'before_sha256': digest(before), 'after_sha256': digest(after),
                         'changed': before != after, 'diff': diff[:18000], 'diff_truncated': len(diff) > 18000})
    if not any(p['changed'] for p in previews):
        raise ValueError('No changed files; nothing to deploy')
    save_plan(plan)
    return {'plan_id': plan['id'], 'status': 'prepared', 'files': previews,
            'note': 'Review diff before apply. Live configuration has not changed.'}


def verify_hashes(plan, side):
    for entry in plan['files']:
        if digest(read_bytes(safe_path(entry['path']))) != entry[side + '_sha256']:
            raise ValueError('Live drift detected: ' + entry['path'])


def write_version(entry, side):
    path = safe_path(entry['path'])
    content = entry[side]
    if content is None:
        path.unlink(missing_ok=True)
    else:
        atomic_write(path, base64.b64decode(content), entry['mode'])
    if digest(read_bytes(path)) != entry[side + '_sha256']:
        raise ValueError('Read-back mismatch: ' + entry['path'])


def apply_plan(plan_id, domains):
    # Validate the reload request before any file mutation.
    if not isinstance(domains, list) or not set(domains) <= RELOADS:
        raise ValueError('Unsupported reload domain')
    plan = get_plan(plan_id)
    if plan['status'] != 'prepared' or time.time() - plan['created'] > 3600:
        raise ValueError('Plan is not prepared or has expired (one hour)')
    if pending_recovery():
        raise ValueError('Interrupted deployment must be recovered first')
    verify_hashes(plan, 'before')
    config_check()  # Never build on an already-invalid live configuration.
    plan['status'] = 'applying'
    save_plan(plan)
    written = []
    try:
        for entry in plan['files']:
            # Recheck immediately before each write, including unchanged entries.
            if digest(read_bytes(safe_path(entry['path']))) != entry['before_sha256']:
                raise ValueError('Concurrent change: ' + entry['path'])
            written.append(entry)
            write_version(entry, 'after')
        verify_hashes(plan, 'after')
        validation = config_check()
    except Exception as exc:
        try:
            for entry in reversed(written):
                actual = digest(read_bytes(safe_path(entry['path'])))
                if actual not in {entry['before_sha256'], entry['after_sha256']}:
                    raise ValueError('Concurrent edit prevents automatic restore')
                write_version(entry, 'before')
            plan['status'] = 'validation_failed_restored'
        except Exception:
            plan['status'] = 'recovery_required'
        save_plan(plan)
        return {'deployment_id': plan_id, 'status': plan['status'], 'error': str(exc),
                'reloads': 'not attempted'}
    plan['status'] = 'applied'
    save_plan(plan)
    reloads = reload_domains(domains)
    plan['reloads'] = reloads
    save_plan(plan)
    return {'deployment_id': plan_id, 'status': plan['status'], 'validation': validation,
            'reloads': reloads, 'restart_performed': False,
            'note': 'Files verified. Behavior and restart-only changes need separate verification.'}


def rollback(plan_id, domains):
    if not isinstance(domains, list) or not set(domains) <= RELOADS:
        raise ValueError('Unsupported reload domain')
    plan = get_plan(plan_id)
    if plan['status'] not in {'applied', 'applying', 'rolling_back', 'recovery_required'}:
        raise ValueError('Deployment cannot be rolled back from this state')
    # Recover interrupted writes only if each file is an exact known version.
    for entry in plan['files']:
        if digest(read_bytes(safe_path(entry['path']))) not in {entry['before_sha256'], entry['after_sha256']}:
            raise ValueError('Concurrent edit prevents rollback: ' + entry['path'])
    plan['status'] = 'rolling_back'
    save_plan(plan)
    for entry in reversed(plan['files']):
        write_version(entry, 'before')
    verify_hashes(plan, 'before')
    validation = config_check()
    plan['status'] = 'rolled_back'
    save_plan(plan)
    return {'deployment_id': plan_id, 'status': 'rolled_back', 'validation': validation,
            'reloads': reload_domains(domains)}


def dispatch(operation, args):
    if operation == 'health':
        core = api('core/info')['data']
        api_config = api('core/api/config')
        return {'core_version': core['version'], 'api_version': api_config['version'],
                'config_access': CONFIG.is_dir(), 'recovery_required': pending_recovery()}
    if operation == 'automations':
        query = args.get('query', '').lower()
        states = api('core/api/states')
        return [{'entity_id': e['entity_id'], 'state': e['state'],
                 'name': e['attributes'].get('friendly_name'), 'item_id': e['attributes'].get('id'),
                 'last_triggered': e['attributes'].get('last_triggered')}
                for e in states if e['entity_id'].startswith('automation.') and
                query in (e['entity_id'] + ' ' + e['attributes'].get('friendly_name', '')).lower()]
    if operation in {'traces_list', 'trace_get'}:
        domain = args.get('domain', 'automation')
        if domain not in {'automation', 'script'}:
            raise ValueError('Trace domain must be automation or script')
        msg = {'type': 'trace/list' if operation == 'traces_list' else 'trace/get',
               'domain': domain, 'item_id': args['item_id']}
        if operation == 'trace_get':
            msg['run_id'] = args['run_id']
        return websocket_command(msg)
    if operation == 'logs':
        lines = args.get('lines', 100)
        if type(lines) is not int or not 1 <= lines <= 500:
            raise ValueError('Log line limit must be 1–500')
        source = args.get('source', 'core')
        if source not in {'core', 'supervisor'}:
            if not re.fullmatch(r'addon:[a-z0-9_]+', source):
                raise ValueError('Use core, supervisor, or addon:slug')
            source = 'addons/' + source.split(':')[1]
        result = api(source + '/logs?lines=' + str(lines), text=True)
        return {'source': args.get('source', 'core'), 'text': '\n'.join(result.splitlines()[-lines:])[-100000:]}
    if operation == 'file_read':
        data = read_bytes(safe_path(args['path']))
        return {'path': args['path'], 'sha256': digest(data),
                'content': None if data is None else data.decode('utf-8')}
    if operation == 'config_check':
        return config_check()
    if operation == 'deploy_prepare':
        return prepare(args['files'])
    if operation == 'deploy_apply':
        return apply_plan(args['plan_id'], args.get('reload_domains', []))
    if operation == 'deploy_rollback':
        return rollback(args['deployment_id'], args.get('reload_domains', []))
    raise ValueError('Unknown operation')


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # No request payloads, traces, credentials, or logs in our own logs.

    def do_POST(self):
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if self.path != '/call' or not 0 < size <= MAX_BODY:
                raise ValueError('Invalid request')
            req = json.loads(self.rfile.read(size))
            value = dispatch(req['operation'], req.get('arguments', {}))
            result = {'ok': True, 'result': redact(value)}
        except Exception as exc:
            result = {'ok': False, 'error': redact(str(exc))}
        body = json.dumps(result).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Server(socketserver.UnixStreamServer):
    # Serial requests prevent overlapping deployments from multiple MCP clients.
    pass


if __name__ == '__main__':
    os.umask(0o077)
    DATA.mkdir(parents=True, exist_ok=True)
    Path(SOCKET).unlink(missing_ok=True)
    with Server(SOCKET, Handler) as server:
        os.chmod(SOCKET, 0o600)
        print('Codex HA Admin ready on local Unix socket', flush=True)
        server.serve_forever()
