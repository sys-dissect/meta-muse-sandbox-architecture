# Meta Muse Systems Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2024.04%20%7C%20Linux%207.0-informational.svg)](part1-the-cage/)
[![Isolation](https://img.shields.io/badge/Isolation-Cloud%20Hypervisor%20%2B%20nspawn-orange.svg)](part1-the-cage/)
[![Engine](https://img.shields.io/badge/Engine-100%20Rust%20Binaries%20%7C%20mold-blueviolet.svg)](part2-the-machinery/)
[![Security Plane](https://img.shields.io/badge/Security-Sentinel%20Daemon%20(Out--of--Band)-red.svg)](part3-the-mind/)
[![Methodology](https://img.shields.io/badge/Methodology-Black--Box%20Verification-brightgreen.svg)](part1-the-cage/evidence/)

> Meta published the blueprint. We measured the building.<br>
> Independent black-box verification of Meta's published Secure VM architecture, with new measurements from inside the runtime cell (`htch-runtime`).

---

## What's New Here

While Meta published their high-level Secure VM design (Sept 8, 2026), this repository provides first-of-its-kind empirical measurements and observed runtime behaviors from inside the workload cell:

1. **Synthetic DNS VIP Allocation:** RFC 2544 benchmark supernet (`198.18.0.0/15`) dynamically mapped to external hosts, returning `NOERROR` even for non-existent domains.
2. **Egress CA Certificate Details:** On-the-fly TLS inspection and re-signing verified via locally installed per-instance egress CA trust anchors.
3. **AF_VSOCK Hypervisor Channel:** Confirmed connectivity to CID 2 (the hypervisor host) on port 512, identifying the narrow guest-host boundary.
4. **Transparent Compression Accounting:** 2 GB of zeroes written to `/var/cache/apt/archives` consumed only ~58 MB of physical storage, verifying Btrfs `compress-force=zstd:3` overmount behavior.
5. **The 100-Binary Suite & Multi-Call Engine:** Full static dissection of `/opt/hatch/bin/`, discovering the 17-applet `hatch-multicall` architecture (Inode 1062), `spawnd` eBPF gatekeeping, and pure Rust 1.97.1 toolchain.
6. **Observed Sentinel Interception:** Empirical capture of real-time stream scrubbing and transcript excision when credentials were leaked during diagnostics, forcing an immediate out-of-band agent re-steering.

---

## Overview

This repository provides an empirical, non-invasive verification of **Meta Muse** (built on the internal Hatch platform runtime). Rather than analyzing static tool definitions or prompt wrappers, this research verifies the architecture from within the live runtime cell across three tracks:

1. **The Sandbox & Hypervisor Confinement ([Track 1: The Cage](part1-the-cage/)):** How untrusted agent code runs with container root privileges while strictly isolated via user namespaces (`uid 0 -> 131072`), Seccomp BPF filters, Btrfs zstd overmounts, RFC 2544 synthetic DNS (`198.18.0.0/15`), and transparent egress proxies.
2. **The Binary Engine & IPC Machinery ([Track 2: The Machinery](part2-the-machinery/)):** The full 100-binary suite, the 17-applet `hatch-multicall` memory deduplication architecture, `spawnd` lifecycle and eBPF cgroup supervisor, `hatch-execd` subprocess cgroups, and the 38+ Unix domain socket matrix.
3. **The Cognitive Engine & Sentinel Security ([Track 3: The Mind](part3-the-mind/)):** How enterprise autonomous agents evolve across multi-frequency asynchronous cadences (hourly memory consolidation, overnight goal studying, and nightly self-healing "dreaming" passes), shell hook event throttling (`silent()` vs `wake()`), and out-of-band Sentinel egress screening.

---

## Related Work

This research builds on and cross-verifies earlier disclosures, binary teardowns, and investigative reporting:

### Official Architecture
- **Meta, "Security and safety for AI agents: our approach with Muse"** (research.meta.ai, Sept 8, 2026): The canonical architecture disclosure describing the Secure VM, `systemd-nspawn` runtime cell, Sentinel as sole egress authority, and credential surrogation.
  *What this repo adds:* Empirical verification from inside the running cell, mapping theoretical boundaries to exact syscall filters, network routes, and storage quotas.

### Independent Teardowns & Incidents
- **Hatch Engine Binary Teardown** ([Gist by @simonpure](https://gist.github.com/simonpure/d6f960045334453360eff1e2a0ebda1e)): Static reverse-engineering of an isolated single `hatch` binary, identifying 38 Unix sockets and JARVIS codenames.
  *What this repo adds:* Simon Pure analyzed only one 332 MB executable. Our work maps the entire **100-binary ecosystem**, the `hatch-multicall` architecture, the `spawnd` supervisor, and combines static binary extraction with live in-situ runtime verification from inside the running cell.
- **macOS Client Teardown** ([muse-endo-teardown by @barkleesanders](https://github.com/barkleesanders/muse-endo-teardown)): Teardown of the Endo desktop client, 51-command device catalog, and Noise-encrypted WebSocket connection to per-user cloud VMs (measured 2026-09-17).
  *What this repo adds:* Focus on the cloud guest and container internals rather than client-side IPC.
- **Sandbox Export Incident** ([ai-tldr.dev report](https://ai-tldr.dev/releases/mousedev-muse-runtime-export/)): 6.8 GB runtime filesystem export via Google Drive (HN front page, 204 pts; closed as N/A by Meta).
  *What this repo adds:* Non-invasive, in-situ systems diagnostics of the live running runtime without bulk exfiltration.

### Secondary Analyses & Reporting
- **Jahanzaib.ai Architecture Breakdown** ([jahanzaib.ai](https://www.jahanzaib.ai/blog/meta-muse-personal-ai-agent-security-architecture)): Summary of Meta's post, highlighting `io_uring` removal, capability stripping (`CAP_SYS_PTRACE`, `CAP_NET_ADMIN`), and containerized credentials.
  *What this repo adds:* Direct syscall probe matrices verifying `io_uring` denial and exact capability masks.
- **Forkast News Sentinel Analysis** ([forkast.news](https://forkast.news/metas-muse-agent-lives-behind-a-kernel-level-sentinel-the-architecture-reveals-where-agent-security-is-heading/)): Deep dive into Sentinel's kernel-level design, eBPF taint tracking, and credential surrogation (Sept 24, 2026).
  *What this repo adds:* Empirical capture of in-flight Sentinel output scrubbing and transcript excision during active agent execution.
- **Ranzware Host Hardware Profiling** ([ranzware.com](https://ranzware.com/meta-muse-runs-agents-on-amd-epyc-turin-hosts-with-two-cores-and-8gb-of-memory)): Reported host specs (AMD EPYC Turin 9D25, 2 cores, 8 GB RAM, Ubuntu 24.04, Linux 7.0).
  *What this repo adds:* In-guest `/proc/cpuinfo`, DMI, and KVM hypervisor flag confirmation matching these specs.
- **The Information / Business Standard Reporting** ([Business Standard](https://www.business-standard.com/amp/technology/artificial-intelligence/how-ai-agent-risks-are-moving-from-developer-sandboxes-to-consumers-126090800873_1.html)): Investigative coverage of the "hard gate" authorization model and credential-vault design.
  *What this repo adds:* In-product observation of how the cognitive loop, shell hooks, and Sentinel interact with the hard gate in real-world agent execution.

---

## Repository Structure

```
├── part1-the-cage/                  # Track 1: Systems & Confinement Whitepaper
│   ├── README.md                    # Full 17-section whitepaper (Inside the Sandbox)
│   ├── evidence/                    # Raw empirical probe logs & audit gap closure reports
│   │   ├── audit-gap-closure-report.md
│   │   ├── sandbox-telemetry-audit.md
│   │   └── vm-boundary-probe-report.md
│   └── tools/                       # Reproduction tooling
│       ├── tailscale_ssh_proxy.py   # Port 3130 stdio CONNECT tunnel helper
│       └── README.md
├── part2-the-machinery/             # Track 2: Binary Architecture, Multicall & IPC Whitepaper
│   ├── README.md                    # 100-binary suite, multicall dispatch, spawnd & IPC matrix
│   └── data/                        # Extracted JSON schemas, crate deps, metrics & help dumps
│       ├── applet_dispatch.json
│       ├── crates.json
│       ├── ebpf.json
│       ├── inventory_table.md
│       ├── metrics.json
│       ├── routes_by_binary.json
│       ├── sockets_by_binary_v2.json
│       ├── tls.json
│       └── help/
└── part3-the-mind/                  # Track 3: Cognitive Engine & Sentinel Whitepaper
    ├── README.md                    # Multi-cadence loops, dreaming, and Sentinel security
    └── references/                  # Sanitized architecture references
        ├── alignment_synthesis_sample.md
        ├── hatch_hook_runtime.sh    # silent() vs wake() event throttling wrapper
        ├── inferred_goal_leads_sample.md
        └── self_improvement.md
```

* 📁 [**Part 1: The Cage — Sandbox Confinement, Storage & Network Mediation**](part1-the-cage/README.md)
  * Full 17-section systems whitepaper covering the Cloud Hypervisor / KVM guest, `systemd-nspawn` cell, syscall error profile, Btrfs zstd `/dev/mapper/rv` overmounts, RFC 2544 synthetic DNS VIP pool, and the Port 3130 Tailscale CONNECT proxy.
  * [Raw Diagnostic Evidence Logs](part1-the-cage/evidence/)
  * [Standalone Reproduction Tools](part1-the-cage/tools/README.md) (including `tailscale_ssh_proxy.py`)

* 📁 [**Part 2: The Machinery — Binary Architecture, Multi-Call Sub-Agents & IPC Topography**](part2-the-machinery/README.md)
  * Complete systems whitepaper on the 100-binary `/opt/hatch/bin/` suite, Inode 1062 `hatch-multicall` deduplication, `spawnd` eBPF cgroup gates, `hatch-execd` socket activation, toolchain verification, and the 38+ socket IPC matrix.
  * [Extracted Datasets & Schemas](part2-the-machinery/data/) (crate graph, sockets, route tables, eBPF rules, metrics)

* 📁 [**Part 3: The Mind — Cognitive Cadences, State Loops & Sentinel Security**](part3-the-mind/README.md)
  * Autonomous agent systems whitepaper deconstructing the multi-frequency cognitive daemons, nightly alignment synthesis, latent goal inference engine (`INFERRED_GOAL_LEADS`), shell hook throttling (`silent()` vs `wake()`), and Sentinel IPC architecture.
  * [Architecture References](part3-the-mind/references/) (sanitized cognitive engine schemas and hook runtime)

---

## About `sys-dissect`

**sys-dissect** is an independent systems research initiative dedicated to the empirical dissection, boundary verification, and containment analysis of production AI runtimes and autonomous agent infrastructure.

### Research Principles
- **Measure Runtime Realities:** Architecture blueprints and design disclosures present intended models; empirical probing verifies actual kernel filters, hypervisor mediation, and storage behavior.
- **Zero-Trust Boundary Analysis:** Model token streams and prompt wrappers are never trusted for authorization; isolation guarantees must be physically enforced out-of-band by the operating system, container runtime, and hypervisor.
- **Responsible & Non-Invasive:** All diagnostics are conducted via bounded, black-box inspection inside authorized workload sessions. No exploits are staged, no host boundaries are breached, and all proprietary tokens or user telemetry are strictly sanitized before publication.

---

## Methodology & Safety

All findings were obtained via non-invasive, black-box diagnostic probing from within an authorized container session. No exploits were attempted, no host boundaries were breached, and no external services were disrupted.

All proprietary session identifiers, internal hostnames (`*.metaaivm.com`), access tokens, and personal user context have been rigorously scrubbed and de-identified.

---

## License & Attribution

Published by [sys-dissect](https://github.com/sys-dissect). Released under the MIT License.
