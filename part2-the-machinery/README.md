# The Machinery: Binary Architecture, Multi-Call Sub-Agents, and IPC Topography of Meta Hatch

**Author:** [sys-dissect](https://github.com/sys-dissect)  
**Target Environment:** Meta Muse / Hatch Autonomous Agent Platform (`htch-runtime`)  
**Methodology:** Passive static analysis, ELF header inspection, and string extraction across `/opt/hatch/bin/`  
**Datasets:** [`part2-the-machinery/data/`](data/)  

---

## 1. Executive Summary

While prior third-party teardowns (such as the [Simon Pure teardown](https://gist.github.com/simonpure/d6f960045334453360eff1e2a0ebda1e)) examined only a single isolated 332 MB `hatch` daemon binary, the live production runtime environment (`htch-runtime`) actually executes an orchestration of **100 distinct ELF binaries** mounted from an immutable Squashfs block device (`/dev/mapper/opt_hatch`, 814 MB read-only).

This whitepaper provides the first comprehensive dissection of the entire `/opt/hatch/bin/` suite:
1. **The Multi-Call Consolidation Architecture (`hatch-multicall`):** 17 primary sub-agent tools (`web-search`, `media-generation`, `tts`, `edits`, `shopping`, `device-data`, `muse-mail`) are hardlinked to a single **29.66 MB binary** (Inode 1062), sharing memory pages across container forks.
2. **The Lifecycle & Confinement Supervisor (`spawnd`):** Uncovers the supervisor subcommands (`attach-cell-gate`, `attach-veth-filter`) that attach `cgroup/connect4` and `cgroup/connect6` eBPF bytecode to enforce fail-closed network policies.
3. **Isolated Execution Daemons (`hatch-execd`, `browser-broker`):** Documents how subprocesses run under dedicated cgroups via systemd socket activation, and why the browser broker socket is deliberately unmounted from the runtime cell to enforce human-in-the-loop (HiTL) consent.
4. **Universal Modern Toolchain:** Empirically proves that 100% of the 100 binaries are written in **Rust 1.97.1**, linked with **mold 2.42.1** on glibc 2.39 with Full RELRO + PIE + NX (and corrects the misconception that `hatch` requires `libstdc++`).
5. **Complete IPC Topography:** Details the directional client/server matrix for all 38+ Unix Domain Sockets under `/run/hatch/` and documents the complete HTTP/WebSocket route tree.

---

## 2. Inode & Packaging Architecture

```
/opt/hatch/bin/ (100 total ELF binaries)
├── Inode 1062: hatch-multicall (29.66 MB, 17 hardlinks in bin/)
│   ├── authdc                     ──> Debug client for /run/hatch/auth/authd.sock
│   ├── browser-service            ──> In-cell DOM capture and browser automation
│   ├── device-data                ──> Paired client device telemetry ingest
│   ├── edits                      ──> High-level code mutation engine
│   ├── feature-request            ──> Telemetry & feedback collector
│   ├── geocode                    ──> Coordinates-to-address resolver
│   ├── hatch-multicall            ──> Multi-call dispatcher entrypoint
│   ├── image-search               ──> Multimodal visual query engine
│   ├── media-generation           ──> Media synthesis client
│   ├── media-library              ──> Local asset and voice memo catalog
│   ├── muse-mail                  ──> Local mailbox ingestion (crate: hatch-email)
│   ├── privsep-test-fully-isolated──> Sandbox privilege verification (crate: privsep-test)
│   ├── share                      ──> Cloudflare tunnel artifact sharing
│   ├── shopping                   ──> Product search & checkout (crate: shopping-cli)
│   ├── subscription-status        ──> User tier & billing entitlement verification
│   ├── tts                        ──> Voice synthesis engine (crate: tts-cli)
│   └── web-search                 ──> Outbound Sentinel-screened search engine
└── Inodes 1058–1200: 83 Standalone Executables
    ├── Infrastructure Orchestrators (hatch, spawnd, hatch-execd, browser-broker, hatch-vault, etc.)
    └── Standalone SaaS Connectors (asana, github, notion-cli, slack, stripe, etc.)
```

### Why Multi-Call?
In a constrained 2 vCPU / 8 GB RAM container cell, launching independent runtime processes for every tool call would induce severe memory pressure and cache thrashing. By consolidating 17 applets into `hatch-multicall`:
* **Page Cache Deduplication:** The Linux kernel shares the clean read-only text segment of Inode 1062 across all concurrent tool invocations.
* **Cold-Start Latency:** The binary remains warm in kernel page caches.
* **Internal Crate Dispatches:** Binary symbols reveal that public tool names are dispatched to internal Cargo workspace crates:
  * `muse-mail` dispatches to crate `hatch-email` (handling `muse-mail-mailbox-v1` and `muse-mail-request-v2` wire formats).
  * `privsep-test-fully-isolated` dispatches to crate `privsep-test`.
  * `shopping` dispatches to crate `shopping-cli`.
  * `tts` dispatches to crate `tts-cli` (generating audio chunks via shortwave RPC).

*(Full applet-to-crate mappings are preserved in [`data/applet_dispatch.json`](data/applet_dispatch.json).)*

---

## 3. Core Infrastructure Daemons

### `spawnd` — Container Supervisor & eBPF Gatekeeper (17.93 MB)
`spawnd` is the host and container lifecycle engine that bootstraps and polices the runtime cell. Unlike generic container runtimes, `spawnd` contains hardcoded security enforcement subcommands:
* `attach-cell-gate`: Attaches fail-closed `cgroup/connect4` and `cgroup/connect6` eBPF programs directly to the container's systemd slice. Any connection attempt to host-local addresses is dropped in the kernel before reaching the network interface.
* `attach-veth-filter`: Attaches an ingress classifier to the host side of the veth interface (`ve-htch-runtime`), dropping frames aimed at host-local services while passing proxy (`3128/3130`) and DNS (`53`) traffic.
* `scrub-env-override`: Renders a sanitized copy of `/etc/hatch/env.override` with secrets stripped before mounting into the cell.
* `prepare-privsep-workers` & `ensure-worker-accounts`: Reconciles dedicated `hatch-w-<tool>` user accounts under the shadow database lock and builds idmapped state views under `/run/hatch/worker-state/<tool>`.
* `verify-contract`: Emits cryptographic contract metadata and JSON schemas validating that runtime boundaries are intact.

### `hatch-execd` — Socket-Activated Subprocess Isolation (8.83 MB)
`hatch-execd` brokers all command-line tool execution requested by the agent:
* **Activation:** Requires `--socket <PATH>` or systemd socket activation via `LISTEN_FDS` (`com.hatch.execd.sock` / `com.hatch.execd-taint.sock`).
* **Cgroup Confinement:** Subprocesses are launched under isolated tool cgroups (`/sys/fs/cgroup/hatch.slice/...`).
* **Taint Tracking:** Interacts with `execd-taint.sock` to propagate data provenance and taint tags from executed subprocess outputs back into the cognitive loop.

### `browser-broker` — Out-of-Band Browser Isolation (18.72 MB)
`browser-broker` routes browser automation sessions to leased VMVM Chromium instances:
* **The HiTL Consent Gate:** `/run/hatch/browser-broker/browser-broker.sock` is **deliberately excluded from the cell bind-mount**. The runtime cell has no filesystem path to the broker.
* **Authentication:** The host daemon connects using exact cgroup identity and `SO_PEERCRED` checks (`--allowed-peer-uid`).
* **Lease Helper:** Uses `hatch-browser-lease-helper` (`helper.sock`) to relay privileged lease operations to `stefi-proxy` and establish viewer bind-mounts.

### `hatch-vault` — CVM Cryptographic Vault (10.33 MB)
* Manages the Root Volume LUKS encryption key (`/run/hatch/vault/rv.key`).
* Communicates with AMD SEV-SNP / Confidential VM attestation layers via `/run/hatch/vault/cvm.sock` and `/run/hatch/vault-encrypt/encrypt.sock`.
* Enforces notary token authentication (`/etc/yolk/notary_public_key`).

### `hatch-rescue` & `hatch-rescue-systemctl` — Emergency Out-of-Band Plane (14.83 MB)
* When the core runtime encounters catastrophic failure, `hatch-rescue` launches a fallback recovery console over WebSockets (`/run/hatch/rescue/ws.sock`) and HTTP (`/run/hatch/rescue/http-api.sock`).
* `hatch-rescue-systemctl` acts as a constrained shim allowing unit inspection and recovery without exposing full D-Bus to the agent.

---

## 4. Toolchain, Hardening & Crate Ecosystem

### Compiler & Binary Hardening
Every binary in `/opt/hatch/bin/` was inspected via `readelf`, `file`, and `strings`:
* **Compiler:** `rustc 1.97.1 (commit 8bab26f4f 2026-07-14)`.
* **Linker:** `mold 2.42.1 (compatible with GNU ld)`.
* **Base C ABI:** GNU C Library 2.39 (`Ubuntu 13.3.0-6ubuntu2~24.04.1`).
* **ELF Hardening Flags:**
  * `PIE`: Full Position Independent Executable.
  * `RELRO`: `GNU_RELRO` present with `BIND_NOW STATIC_TLS`.
  * `Stack`: `GNU_STACK RW 0x1` (No-eXecute memory protection).
  * `Symbols`: Stripped `.symtab`.

### Fact Check: The `libstdc++` Myth
Prior reports (Simon Pure gist) claimed that the `hatch` daemon is dynamically linked against `libstdc++.so.6`. Empirical dependency inspection via `readelf -d /opt/hatch/bin/hatch` refutes this:
```text
Dynamic section at offset 0x153fd7a8 contains 34 entries:
  Tag        Type                         Name/Value
 0x00000001 (NEEDED)                     Shared library: [libelf.so.1]
 0x00000001 (NEEDED)                     Shared library: [libz.so.1]
 0x00000001 (NEEDED)                     Shared library: [libgcc_s.so.1]
 0x00000001 (NEEDED)                     Shared library: [libm.so.6]
 0x00000001 (NEEDED)                     Shared library: [libc.so.6]
 0x00000001 (NEEDED)                     Shared library: [ld-linux-x86-64.so.2]
```
There is **zero C++ runtime linkage**. The entire stack is native Rust with direct glibc bindings.

### Key Embedded Crates Discovered
Extraction from `.rodata` and panic location traces ([`data/crates.json`](data/crates.json)) identifies the core architectural blocks:
* **In-Process JavaScript Engine (`boa_engine 0.21.1`):** Hatch embeds a pure-Rust ECMAScript engine to execute untrusted client scripts and template expressions in-process without invoking an external Node/V8 runtime.
* **Local Lexical Search (`bm25 2.3.2`):** Implements in-memory BM25 ranking for local contextual retrieval, allowing the agent to perform fast document search over memory stores without calling remote embeddings.
* **Native Document Parsing (`calamine 0.36.1`):** Pure-Rust parser for Excel, OpenDocument, and CSV spreadsheets.
* **Storage & HTTP Layer:** Built on `axum 0.8.9`, `sqlx 0.8.6` (PostgreSQL), and `tokio-tungstenite 0.29.0` (WebSockets).

---

## 5. IPC Topography & Socket Matrix

All inter-process communication is decoupled across 38+ Unix Domain Sockets beneath `/run/hatch/`:

| Component / Subsystem | Socket Path | Direction | Observed Protocol | Confinement & Access Model |
| :--- | :--- | :--- | :--- | :--- |
| **Sentinel Daemon** | `/run/hatch/sentinel/http-api.sock` | Listener | HTTP / REST | Egress security authority. Validates request tokens and policies. |
| **Sentinel Approvals** | `/run/hatch/sentinel/egress-approvals.sock` | Listener | Stream RPC | Egress approval requests; triggers out-of-band user approval cards. |
| **Sentinel Admin** | `/run/hatch/sentinel/egress-approvals-admin.sock` | Listener | Stream RPC | Administrative approval channel; restricted to host-root. |
| **Daemon Approvals Event** | `/run/hatch/daemon/egress-approvals-events.sock` | Bidirectional | Event Stream | Broadcasts live approval resolution events back to the `hatch` core daemon. |
| **Auth Daemon (authd)** | `/run/hatch/auth/authd.sock` | Listener | HTTP / REST | Credential surrogation (`/v1/credentials/surrogate`, `/v1/auth-file/*`). Gates calls with `SO_PEERCRED`. |
| **Exec Daemon (execd)** | `/run/hatch/daemon/execd.sock` | Listener | Socket-Activated | Spawns bash processes in dedicated tool cgroups. Managed via systemd `LISTEN_FDS`. |
| **Execd Taint Tracker** | `/run/hatch/daemon/execd-taint.sock` | Listener | Stream IPC | Informs execd and daemon of runtime taint propagation. |
| **Daemon Metrics** | `/run/hatch/daemon/metrics.sock` | Listener | HTTP (`/metrics`, `/health`) | Polled by `hatch-healthd` from host side without traversing veth. |
| **Browser Broker** | `/run/hatch/browser-broker/browser-broker.sock` | Listener | Custom RPC | Routes browser sessions. **Intentionally unmounted** in the cell to prevent HiTL bypass. |
| **Browser Lease Helper** | `/run/hatch/browser-lease-helper/helper.sock` | Listener | Privileged RPC | Intermediary for `browser-broker` to interact with `stefi-proxy`. |
| **Vault Auth** | `/run/hatch/vault/auth.sock` | Listener | HTTP / Notary | Authenticates root volume decryption requests using notary tokens. |
| **Vault CVM & Health** | `/run/hatch/vault/cvm.sock`<br>`/run/hatch/vault/health.sock` | Listener | Stream IPC | Reports confidential VM hardware security status and key enrollment. |
| **Vault Crypto** | `/run/hatch/vault-encrypt/encrypt.sock`<br>`/run/hatch/vault-hmac/hmac.sock` | Listener | Binary RPC | Cryptographic offload for attestation sealing and HMAC generation. |
| **Inference Proxy** | `/run/hatch/proxy/inference.sock` | Client $\to$ Srv | HTTP / SSE | Proxies model inference calls (`JARVIS_INFERENCE_PROXY_SOCK`). Enforces token quotas. |
| **Stefi Integration Proxy** | `/run/hatch/proxy/stefi.sock` | Client $\to$ Srv | HTTP / REST | Gateway for external SaaS callbacks, payment transactions, and avatar media tasks. |
| **Node Daemon (noded)** | `/run/hatch/noded/http-api.sock`<br>`/run/hatch/noded/control.sock` | Listener | HTTP / JSON RPC | Host node orchestrator managing runtime containers and ephemeral workspaces. |
| **Rescue Console** | `/run/hatch/rescue/http-api.sock`<br>`/run/hatch/rescue/ws.sock` | Listener | HTTP / WebSocket | Out-of-band console powered by `tokio-tungstenite` for emergency recovery. |
| **Storage Recovery** | `/run/hatch/storage-recovery/filesystem.sock`<br>`/run/hatch/storage-recovery/http-api.sock` | Listener | Binary / HTTP | Filesystem state reconstruction and Btrfs snapshot reconciliation. |
| **Telemetry & Scuba** | `/run/hatch/telemetry/telemetry.sock`<br>`/run/hatch/telemetry/bugreport.sock` | Listener | Stream IPC | Ingestion sink for Scuba telemetry events and crash bugreports. |
| **Companion Daemons** | `/run/hatch/wai/wai.sock`<br>`/run/hatch/whatsapp-companion/companion.sock` | Listener | Custom IPC | WhatsApp and companion hardware sync channels. |
| **Privilege-Separated Tools**| `/run/hatch/privsep/<tool>.sock` | Listener | Isolated IPC | Dedicated worker sockets (`oura.sock`, `strava-cli.sock`, `square.sock`, etc.) owned by `hatch-w-<tool>`. |

*(Full per-binary socket mappings are detailed in [`data/sockets_by_binary_v2.json`](data/sockets_by_binary_v2.json).)*

---

## 6. What Was Previously Unknown: Comparative Matrix

| Architectural Feature | Simon Pure Teardown (Gist) | Meta Published Architecture (Sept 2026) | sys-dissect (This Research) |
| :--- | :--- | :--- | :--- |
| **Scope of Inspection** | Single 332 MB `hatch` binary in isolation | High-level marketing/blog post | **Complete 100-binary suite in `/opt/hatch/bin/`** |
| **Multi-Call Packaging** | Not mentioned | Not mentioned | **Documented Inode 1062 (`hatch-multicall`), 17 sub-agent tools, and applet crate mapping** |
| **Supervisor Architecture** | Absent | Mentioned abstractly | **Deconstructed `spawnd` subcommands (`attach-cell-gate`, `attach-veth-filter`)** |
| **Subprocess Execution** | Inferred | Generic mention | **Documented `hatch-execd` systemd socket activation (`LISTEN_FDS`) & tool cgroups** |
| **Browser Broker Isolation** | Assumed to be local socket | Mentioned as leased browser | **Proved broker socket is deliberately excluded from cell bind mount to enforce HiTL consent** |
| **Compiler & ABI** | Inaccurately claimed `libstdc++` | Stated "written in Rust" | **Proved pure Rust 1.97.1 + mold 2.42.1 + glibc 2.39; zero `libstdc++` linkage** |
| **Embedded Engine Crates** | Listed crate names | Unmentioned | **Identified `boa_engine` (in-process JS), `bm25` (lexical search), `calamine` (Excel parsing)** |
| **IPC Topology** | Unstructured strings list | 38 sockets mentioned | **Authoritative directional client/server matrix with protocol definitions** |
| **External/Internal Routes** | Incomplete string snippets | Undisclosed | **Complete route table ([`data/routes_by_binary.json`](data/routes_by_binary.json)) for `/hatch/*`, `/api/*`, `/v1/*`** |

---

## 7. Data Artifacts Index

All extracted empirical datasets are preserved under [`part2-the-machinery/data/`](data/):
* [`inventory_table.md`](data/inventory_table.md): Full markdown inventory of all 100 binaries with sizes and descriptions.
* [`applet_dispatch.json`](data/applet_dispatch.json): Dispatch table mapping multicall tool names to compiled Cargo crate names.
* [`crates.json`](data/crates.json): Complete third-party and internal Rust dependency manifest.
* [`sockets_by_binary_v2.json`](data/sockets_by_binary_v2.json): Per-binary mapping of all Unix Domain Sockets.
* [`routes_by_binary.json`](data/routes_by_binary.json) & [`routes_notes.json`](data/routes_notes.json): Extracted API route definitions and notes.
* [`ebpf.json`](data/ebpf.json): Kernel eBPF program hooks and capability constraints.
* [`tls.json`](data/tls.json): Supported TLS ciphers, protocols, and certificate search paths.
* [`metrics.json`](data/metrics.json): 189 KB catalog of internal Scuba and Prometheus metric counters.
* [`help/`](data/help/): Directory containing raw CLI `--help` text dumps for core binaries.
