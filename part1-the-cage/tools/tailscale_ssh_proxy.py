#!/usr/bin/env python3
"""ProxyCommand helper: bidirectionally forward stdio through the
Tailscale-aware egress proxy (port 3130) to a tailnet host:port."""
import socket, base64, os, sys, select
from urllib.parse import urlparse

def main():
    target_host, target_port = sys.argv[1], sys.argv[2]
    u = urlparse(os.environ["HTTPS_PROXY"])
    proxy_host, proxy_port = u.hostname, 3130
    auth = base64.b64encode(f"{u.username}:{u.password}".encode()).decode()

    s = socket.create_connection((proxy_host, proxy_port), timeout=20)
    s.sendall(
        f"CONNECT {target_host}:{target_port} HTTP/1.1\r\n"
        f"Host: {target_host}:{target_port}\r\n"
        f"Proxy-Authorization: Basic {auth}\r\n\r\n".encode()
    )
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = s.recv(4096)
        if not chunk:
            return 1
        resp += chunk
    if b"200" not in resp.split(b"\r\n")[0]:
        return 1

    s.setblocking(False)
    os.set_blocking(0, False)
    os.set_blocking(1, False)
    net = s.fileno()
    while True:
        r, _, _ = select.select([0, net], [], [])
        if 0 in r:  # ssh -> network
            data = os.read(0, 65536)
            if not data:
                return 0
            s.sendall(data)
        if net in r:  # network -> ssh
            try:
                data = s.recv(65536)
            except BlockingIOError:
                continue
            if not data:
                return 0
            os.write(1, data)
    return 0

sys.exit(main())
