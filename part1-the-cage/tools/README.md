# Tools & Reproduction Helpers

This directory contains standalone utility scripts developed during the non-invasive probing of the Meta Muse / Hatch sandbox environment.

### `tailscale_ssh_proxy.py`
A custom `ProxyCommand` transport helper.

**Problem:**
The Hatch VM environment blocks raw ICMP/UDP and direct TCP packets across the network namespace. Even though the VM enrolls on a Tailnet, direct routing to Tailscale IP ranges (`100.64.0.0/10`) fails.

**Solution:**
The local egress daemon exposes port `3130` specifically for tailnet traffic (`${HTTPS_PROXY%:*}:3130`). This script parses the local proxy credentials from `$HTTPS_PROXY`, negotiates an `HTTP CONNECT` tunnel to the target tailnet host on port 3130, and bidirectionally splices `stdin`/`stdout` with the network socket using non-blocking I/O and `select()`.

**Usage in `~/.ssh/config`:**
```ssh-config
Host example-host
    HostName 100.64.0.x
    User <remote-user>
    ProxyCommand python3 /path/to/tailscale_ssh_proxy.py %h %p
```
