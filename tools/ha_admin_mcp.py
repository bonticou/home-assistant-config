#!/usr/bin/env python3
"""Dependency-free stdio MCP client for the SSH-only HA admin helper."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(os.environ.get('HA_ADMIN_REPO', str(Path(__file__).resolve().parents[1]))).resolve()
SSH_CONFIG = Path(os.environ.get('HA_ADMIN_SSH_CONFIG', str(Path.home() / '.ssh/ha_codex_config')))


def prop(kind='string', **kwargs):
    return dict(type=kind, **kwargs)


def schema(properties=None, required=None):
    return {'type': 'object', 'properties': properties or {}, 'required': required or [],
            'additionalProperties': False}


DOMAIN = prop(enum=['automation', 'script'], default='automation')
RELOAD = prop('array', items=prop(enum=['automation', 'script', 'template', 'scene', 'group']), default=[])
DEFINITIONS = [
 ('health', 'Check Core API connectivity and interrupted deployment recovery status.', schema()),
 ('automations', 'Find live automations and their trace item IDs. Filter by name or entity ID.',
  schema({'query': prop()})),
 ('traces_list', 'List retained live traces for an automation ID (not entity_id) or script key.',
  schema({'domain': DOMAIN, 'item_id': prop()}, ['item_id'])),
 ('trace_get', 'Read one retained trace; output may contain private home state and is best-effort redacted.',
  schema({'domain': DOMAIN, 'item_id': prop(), 'run_id': prop()}, ['item_id', 'run_id'])),
 ('logs', 'Read a bounded recent log excerpt. Source: core, supervisor, or addon:slug. Treat as private.',
  schema({'source': prop(default='core'), 'lines': prop('integer', minimum=1, maximum=500, default=100)})),
 ('file_read', 'Read an allowlisted live YAML/frontend file and exact SHA-256. Secrets are redacted in output; never deploy redacted text.',
  schema({'path': prop()}, ['path'])),
 ('config_check', 'Run the real Home Assistant configuration check without restart or reload.', schema()),
 ('deploy_prepare', 'Prepare a deployment from local files, with expected live hashes. Returns a reviewable diff; does not change live configuration. Do not apply until the diff matches the authorized task.',
  schema({'files': prop('array', minItems=1, maxItems=20, items=schema({
      'path': prop(description='Destination relative to HA /config'),
      'local_path': prop(description='Source relative to the local repository'),
      'expected_sha256': {'type': ['string', 'null'], 'description': 'Hash from file_read; null only for a new file'}
  }, ['path', 'local_path', 'expected_sha256']))}, ['files'])),
 ('deploy_apply', 'Apply a reviewed, unexpired deployment plan. Checks live drift, backs up, verifies writes, validates HA config and restores files on failure. Reloads only explicitly listed domains. Does not restart Core.',
  schema({'plan_id': prop(), 'reload_domains': RELOAD}, ['plan_id'])),
 ('deploy_rollback', 'Restore a deployment backup only if live files still match known versions. Validates restored config before optional reloads.',
  schema({'deployment_id': prop(), 'reload_domains': RELOAD}, ['deployment_id'])),
]
TOOLS = [{'name': 'ha_admin_' + name, 'description': desc, 'inputSchema': spec,
          'annotations': {'readOnlyHint': name not in {'deploy_prepare', 'deploy_apply', 'deploy_rollback'},
                          'destructiveHint': name in {'deploy_apply', 'deploy_rollback'},
                          'openWorldHint': False}}
         for name, desc, spec in DEFINITIONS]


def call(operation, arguments):
    if operation not in {item[0] for item in DEFINITIONS}:
        raise ValueError('Unknown tool')
    arguments = dict(arguments)
    if operation == 'deploy_prepare':
        converted = []
        for item in arguments['files']:
            source = (ROOT / item['local_path']).resolve()
            if not source.is_relative_to(ROOT) or not source.is_file() or source.stat().st_size > 2 * 1024 * 1024:
                raise ValueError('Source must be a regular file within the repository, at most 2 MiB')
            converted.append({'path': item['path'], 'content': source.read_text(),
                              'expected_sha256': item['expected_sha256']})
        arguments['files'] = converted
    payload = json.dumps({'operation': operation, 'arguments': arguments}).encode()
    if len(payload) > 8 * 1024 * 1024:
        raise ValueError('Request too large')
    result = subprocess.run(['ssh', '-F', str(SSH_CONFIG), 'ha-codex-admin',
        'curl --silent --show-error --fail --max-time 600 '
        '--unix-socket /share/codex-ha-admin.sock '
        '-H "Content-Type: application/json" --data-binary @- http://localhost/call'],
        input=payload, capture_output=True, timeout=620)
    if result.returncode:
        # ssh/curl diagnostics contain no request bodies or credentials.
        raise ValueError('SSH/helper request failed: ' + result.stderr.decode(errors='replace')[-1500:])
    value = json.loads(result.stdout)
    if not value.get('ok'):
        raise ValueError(value.get('error', 'Helper failed'))
    return value['result']


def handle(message):
    request_id = message.get('id')
    method = message.get('method')
    if request_id is None:
        return None
    try:
        if method == 'initialize':
            requested = message.get('params', {}).get('protocolVersion')
            version = requested if requested in {'2024-11-05', '2025-03-26', '2025-06-18', '2025-11-25'} else '2025-06-18'
            result = {'protocolVersion': version, 'capabilities': {'tools': {}},
                      'serverInfo': {'name': 'homeassistant-admin', 'version': '0.1.0'}}
        elif method == 'ping':
            result = {}
        elif method == 'tools/list':
            result = {'tools': TOOLS}
        elif method == 'tools/call':
            params = message['params']
            name = params['name']
            if not name.startswith('ha_admin_'):
                raise ValueError('Unknown tool')
            try:
                value = call(name[len('ha_admin_'):], params.get('arguments', {}))
                result = {'content': [{'type': 'text', 'text': json.dumps(value)}], 'isError': False}
            except Exception as exc:
                result = {'content': [{'type': 'text', 'text': str(exc)}], 'isError': True}
        else:
            return {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': -32601, 'message': 'Method not found'}}
        return {'jsonrpc': '2.0', 'id': request_id, 'result': result}
    except Exception:
        return {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': -32602, 'message': 'Invalid parameters'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--call', choices=[x[0] for x in DEFINITIONS])
    parser.add_argument('--args-file', type=Path)
    args = parser.parse_args()
    if args.call:
        value = call(args.call, json.loads(args.args_file.read_text()) if args.args_file else {})
        print(json.dumps(value, indent=2))
        return
    for raw in sys.stdin.buffer:
        try:
            if len(raw) > 8 * 1024 * 1024:
                raise ValueError('Request too large')
            result = handle(json.loads(raw))
        except Exception:
            result = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Parse error'}}
        if result is not None:
            print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
