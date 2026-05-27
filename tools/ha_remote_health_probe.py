#!/usr/bin/env python3
"""Probe Home Assistant Remote UI from outside Home Assistant.

The probe intentionally treats the websocket `auth_required` greeting as a
success: it proves the request reached Trevor's Home Assistant instance before
any long-lived token is needed.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any


FALLBACK_MARKERS = (
    "Unable to connect to Home Assistant",
    "not currently connected",
    "Nabu Casa account page",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def elapsed_ms(start: float) -> int:
    return int((time.monotonic() - start) * 1000)


def normalize_url(raw_url: str) -> str:
    raw_url = raw_url.strip()
    if not raw_url:
        raise ValueError("URL is empty")
    parsed = urllib.parse.urlparse(raw_url)
    if not parsed.scheme:
        raw_url = f"https://{raw_url}"
        parsed = urllib.parse.urlparse(raw_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must start with http:// or https://")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")
    return raw_url.rstrip("/")


def redact_url(raw_url: str) -> str:
    parsed = urllib.parse.urlparse(raw_url)
    port = f":{parsed.port}" if parsed.port else ""
    path = parsed.path if parsed.path and parsed.path != "/" else "/"
    return urllib.parse.urlunparse((parsed.scheme, f"<redacted-host>{port}", path, "", "", ""))


def host_hash(hostname: str) -> str:
    digest = hashlib.sha256(hostname.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:12]}"


def detect_nabu_fallback(text: str) -> bool:
    return any(marker in text for marker in FALLBACK_MARKERS)


def target_summary(url: str) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    default_port = 443 if parsed.scheme == "https" else 80
    return {
        "url": redact_url(url),
        "scheme": parsed.scheme,
        "host_hash": host_hash(parsed.hostname or ""),
        "port": parsed.port or default_port,
    }


def resolve_dns(hostname: str, port: int, timeout: float) -> tuple[list[Any], dict[str, Any]]:
    start = time.monotonic()
    previous_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        infos = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except OSError as exc:
        return [], {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "error": exc.__class__.__name__,
            "message": str(exc),
        }
    finally:
        socket.setdefaulttimeout(previous_timeout)

    families = sorted({socket.AddressFamily(info[0]).name for info in infos})
    return infos, {
        "ok": True,
        "elapsed_ms": elapsed_ms(start),
        "address_count": len(infos),
        "families": families,
    }


def connect_socket(
    infos: list[Any],
    hostname: str,
    timeout: float,
    use_tls: bool,
) -> tuple[socket.socket | ssl.SSLSocket | None, dict[str, Any], dict[str, Any]]:
    tcp_start = time.monotonic()
    last_error = ""
    raw_sock: socket.socket | None = None

    for family, socktype, proto, _canonname, sockaddr in infos:
        try:
            raw_sock = socket.socket(family, socktype, proto)
            raw_sock.settimeout(timeout)
            raw_sock.connect(sockaddr)
            break
        except OSError as exc:
            last_error = f"{exc.__class__.__name__}: {exc}"
            if raw_sock is not None:
                raw_sock.close()
            raw_sock = None

    tcp_result = {
        "ok": raw_sock is not None,
        "elapsed_ms": elapsed_ms(tcp_start),
    }
    if raw_sock is None:
        tcp_result["error"] = last_error or "connect failed"
        return None, tcp_result, {"ok": not use_tls, "elapsed_ms": 0}

    if not use_tls:
        return raw_sock, tcp_result, {"ok": True, "elapsed_ms": 0}

    tls_start = time.monotonic()
    try:
        context = ssl.create_default_context()
        tls_sock = context.wrap_socket(raw_sock, server_hostname=hostname)
        return tls_sock, tcp_result, {"ok": True, "elapsed_ms": elapsed_ms(tls_start)}
    except (OSError, ssl.SSLError) as exc:
        raw_sock.close()
        return None, tcp_result, {
            "ok": False,
            "elapsed_ms": elapsed_ms(tls_start),
            "error": exc.__class__.__name__,
            "message": str(exc),
        }


def http_probe(url: str, timeout: float) -> dict[str, Any]:
    start = time.monotonic()
    request = urllib.request.Request(
        f"{url}/",
        headers={
            "User-Agent": "HA-Remote-Health-Probe/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(262144).decode("utf-8", errors="replace")
            return {
                "ok": 200 <= response.status < 400,
                "elapsed_ms": elapsed_ms(start),
                "status_code": response.status,
                "final_url": redact_url(response.url),
                "content_type": response.headers.get("content-type", ""),
                "fallback_detected": detect_nabu_fallback(body),
                "body_sample": body[:120] if detect_nabu_fallback(body) else "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(262144).decode("utf-8", errors="replace")
        return {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "status_code": exc.code,
            "final_url": redact_url(exc.url),
            "content_type": exc.headers.get("content-type", ""),
            "fallback_detected": detect_nabu_fallback(body),
            "error": "HTTPError",
        }
    except urllib.error.URLError as exc:
        return {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "fallback_detected": False,
            "error": exc.__class__.__name__,
            "message": str(exc.reason),
        }
    except OSError as exc:
        return {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "fallback_detected": False,
            "error": exc.__class__.__name__,
            "message": str(exc),
        }


def read_exact(sock: socket.socket | ssl.SSLSocket, length: int) -> bytes:
    chunks: list[bytes] = []
    remaining = length
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("socket closed before enough data arrived")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_http_headers(sock: socket.socket | ssl.SSLSocket) -> bytes:
    data = bytearray()
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
        if len(data) > 65536:
            raise ValueError("websocket upgrade headers exceeded 64 KiB")
    return bytes(data)


def read_ws_text_frame(sock: socket.socket | ssl.SSLSocket) -> str:
    for _ in range(3):
        first = read_exact(sock, 2)
        opcode = first[0] & 0x0F
        masked = bool(first[1] & 0x80)
        length = first[1] & 0x7F
        if length == 126:
            length = int.from_bytes(read_exact(sock, 2), "big")
        elif length == 127:
            length = int.from_bytes(read_exact(sock, 8), "big")
        if length > 1048576:
            raise ValueError("websocket frame exceeded 1 MiB")
        mask = read_exact(sock, 4) if masked else b""
        payload = read_exact(sock, length) if length else b""
        if masked:
            payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        if opcode == 1:
            return payload.decode("utf-8", errors="replace")
        if opcode == 8:
            raise ConnectionError("websocket closed before greeting")
    raise TimeoutError("did not receive a text websocket greeting")


def websocket_probe(url: str, timeout: float) -> dict[str, Any]:
    start = time.monotonic()
    ws_url = urllib.parse.urljoin(f"{url}/", "api/websocket")
    parsed = urllib.parse.urlparse(ws_url)
    hostname = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    infos, dns = resolve_dns(hostname, port, timeout)
    if not dns.get("ok"):
        return {"ok": False, "elapsed_ms": elapsed_ms(start), "stage": "dns", "dns": dns}

    sock, tcp, tls = connect_socket(infos, hostname, timeout, parsed.scheme == "https")
    if sock is None:
        return {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "stage": "tls" if tcp.get("ok") else "tcp",
            "dns": dns,
            "tcp": tcp,
            "tls": tls,
        }

    key = base64.b64encode(os.urandom(16)).decode("ascii")
    path = parsed.path or "/api/websocket"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "User-Agent: HA-Remote-Health-Probe/1.0\r\n"
        "\r\n"
    ).encode("ascii")

    try:
        sock.sendall(request)
        header_bytes = read_http_headers(sock)
        header_text = header_bytes.decode("iso-8859-1", errors="replace")
        status_line = header_text.splitlines()[0] if header_text else ""
        parts = status_line.split()
        status_code = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else None
        if status_code != 101:
            return {
                "ok": False,
                "elapsed_ms": elapsed_ms(start),
                "stage": "upgrade",
                "dns": dns,
                "tcp": tcp,
                "tls": tls,
                "status_code": status_code,
                "status_line": status_line,
                "fallback_detected": detect_nabu_fallback(header_text),
            }

        greeting = read_ws_text_frame(sock)
        try:
            message = json.loads(greeting)
        except json.JSONDecodeError:
            message = {}
        message_type = message.get("type", "")
        return {
            "ok": message_type == "auth_required",
            "elapsed_ms": elapsed_ms(start),
            "stage": "auth_required" if message_type == "auth_required" else "greeting",
            "dns": dns,
            "tcp": tcp,
            "tls": tls,
            "status_code": status_code,
            "message_type": message_type,
            "ha_version": message.get("ha_version", ""),
        }
    except (OSError, ValueError, ConnectionError, TimeoutError) as exc:
        return {
            "ok": False,
            "elapsed_ms": elapsed_ms(start),
            "stage": "websocket",
            "dns": dns,
            "tcp": tcp,
            "tls": tls,
            "error": exc.__class__.__name__,
            "message": str(exc),
        }
    finally:
        sock.close()


def classify_result(payload: dict[str, Any]) -> str:
    http = payload.get("http", {})
    websocket = payload.get("websocket", {})
    dns = payload.get("dns", {})
    tcp = payload.get("tcp", {})
    tls = payload.get("tls", {})

    if http.get("fallback_detected") or websocket.get("fallback_detected"):
        return "remote_fallback"
    if websocket.get("stage") == "auth_required":
        return "ok"
    if not dns.get("ok"):
        return "dns_error"
    if not tcp.get("ok"):
        return "tcp_error"
    if not tls.get("ok"):
        return "tls_error"
    if http and not http.get("ok"):
        return "http_error"
    if websocket and not websocket.get("ok"):
        return "websocket_error"
    return "unknown"


def build_payload(url: str, timeout: float) -> dict[str, Any]:
    started = time.monotonic()
    parsed = urllib.parse.urlparse(url)
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    infos, dns = resolve_dns(parsed.hostname or "", port, timeout)
    sock, tcp, tls = (None, {"ok": False}, {"ok": False})
    if dns.get("ok"):
        sock, tcp, tls = connect_socket(infos, parsed.hostname or "", timeout, parsed.scheme == "https")
        if sock is not None:
            sock.close()

    payload: dict[str, Any] = {
        "checked_at": now_iso(),
        "target": target_summary(url),
        "dns": dns,
        "tcp": tcp,
        "tls": tls,
        "http": http_probe(url, timeout),
        "websocket": websocket_probe(url, timeout),
        "elapsed_ms": elapsed_ms(started),
    }
    payload["status"] = classify_result(payload)
    payload["ok"] = payload["status"] == "ok"
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Remote HA URL. Defaults to HA_REMOTE_URL.")
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_url = args.url or os.environ.get("HA_REMOTE_URL", "")
    if not raw_url:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "config_missing",
                    "message": "Set HA_REMOTE_URL or pass --url.",
                    "checked_at": now_iso(),
                },
                separators=(",", ":"),
            )
        )
        return 2

    try:
        url = normalize_url(raw_url)
        payload = build_payload(url, args.timeout)
    except ValueError as exc:
        payload = {
            "ok": False,
            "status": "config_error",
            "message": str(exc),
            "checked_at": now_iso(),
        }

    if args.pretty:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
