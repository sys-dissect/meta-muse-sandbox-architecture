# Meta Muse Systems Architecture

> Forensic reverse-engineering, sandbox boundary diagnostics, cognitive cadences, and out-of-band security analysis of Meta's autonomous agent runtime (`htch-runtime`).

---

## Overview

This repository contains an empirical, non-invasive systems analysis of **Meta Muse** (built on the internal Hatch platform runtime). Rather than analyzing static tool definitions or prompt wrappers, this research deconstructs:

1. **The Sandbox & Hypervisor Confinement:** How untrusted agent code runs with container root privileges while strictly isolated via user namespaces (`uid 0 -> 131072`), Seccomp BPF filters, Btrfs zstd overmounts, RFC 2544 synthetic DNS (`198.18.0.0/15`), and transparent egress proxies.
2. **The Cognitive Engine:** How enterprise autonomous agents evolve across multi-frequency asynchronous cadences (hourly memory consolidation, overnight goal studying, and nightly self-healing "dreaming" passes).
3. **The Out-of-Band Security Plane ("Sentinel"):** Why prompt-based permissions fail, and how an independent policy daemon enforces opaque approval cards and live output scrubbing without trusting model token streams.

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
├── part2-the-mind/                  # Track 2: Cognitive Engine & Sentinel Whitepaper
│   ├── README.md                    # Multi-cadence loops, dreaming, and Sentinel security
│   └── references/                  # Sanitized architecture references
│       ├── alignment_synthesis_sample.md
│       ├── hatch_hook_runtime.sh    # silent() vs wake() event throttling wrapper
│       ├── inferred_goal_leads_sample.md
│       └── self_improvement.md
└── articles/                        # Editorial Release
    └── deconstructing-meta-muse-architecture.md  # Condensed technical article
```

* 📁 [**Part 1: The Cage — Sandbox Confinement, Storage & Network Mediation**](part1-the-cage/README.md)
  * Full 17-section systems whitepaper covering the Cloud Hypervisor / KVM guest, `systemd-nspawn` cell, syscall error profile, Btrfs zstd `/dev/mapper/rv` overmounts, RFC 2544 synthetic DNS VIP pool, and the Port 3130 Tailscale CONNECT proxy.
  * [Raw Diagnostic Evidence Logs](part1-the-cage/evidence/)
  * [Standalone Reproduction Tools](part1-the-cage/tools/README.md) (including `tailscale_ssh_proxy.py`)

* 📁 [**Part 2: The Mind — Cognitive Cadences, State Loops & Sentinel Security**](part2-the-mind/README.md)
  * Autonomous agent systems whitepaper deconstructing the multi-frequency cognitive daemons, nightly alignment synthesis, latent goal inference engine (`INFERRED_GOAL_LEADS`), shell hook throttling (`silent()` vs `wake()`), and Sentinel IPC architecture.
  * [Architecture References](part2-the-mind/references/) (sanitized cognitive engine schemas and hook runtime)

* 📄 [**Editorial Article: Deconstructing Meta Muse Architecture**](articles/deconstructing-meta-muse-architecture.md)
  * Condensed architectural teardown and takeaways for enterprise AI platform engineers.

---

## Methodology & Safety

All findings were obtained via non-invasive, black-box diagnostic probing from within an authorized container session. No exploits were attempted, no host boundaries were breached, and no external services were disrupted. 

All proprietary session identifiers, internal hostnames (`*.metaaivm.com`), access tokens, and personal user context have been rigorously scrubbed and de-identified.

---

## License & Attribution

Published by [sys-dissect](https://github.com/sys-dissect). Released under the MIT License.
