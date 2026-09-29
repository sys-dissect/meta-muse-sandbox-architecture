# Sandbox Telemetry & Resource Accounting Audit

Date: 2026-09-29 ~12:05 IST (Asia/Kolkata). Non-destructive, diagnostic only.
No sockets under `/run/hatch/` were connected to; no cgroup files written; no config changed.

## 1. Persistence State

Exact paths checked (`$path/marker`):

| Path | Result |
|------|--------|
| `/home/hatch/marker` | NOT FOUND |
| `/root/marker` | NOT FOUND |
| `/etc/marker` | NOT FOUND |
| `/tmp/marker` | NOT FOUND |
| `/var/tmp/marker` | NOT FOUND |

Supplementary: the `.probe2-marker` files written ~40 min earlier (probe2, section I)
are all still present with identical sha256 (`b3599ca5…0e5b43d`):

- `/home/hatch/.probe2-marker`, `/root/.probe2-marker`, `/etc/.probe2-marker`,
  `/tmp/.probe2-marker`, `/var/tmp/.probe2-marker` — all FOUND, hashes match.

Caveat (FACT): no boundary reset (reboot) occurred between the probe2 writes and
this check — PID 1 (`systemd`) start time is unchanged (07:24 today) and these are
separate shells in one continuous session. So cross-reset persistence is
**NOT DETERMINABLE** from this data; what is confirmed is durability across
exec sessions (fresh shells). The literal `marker` files were simply never created.

## 2. Reconciliation Table (all figures kB, from `/proc/meminfo`)

| Component | kB | Note |
|-----------|----|------|
| MemTotal | 8,126,308 | host-wide figure (no memory cgroup attached) |
| MemFree | 1,188,040 | |
| MemAvailable | 2,716,628 | |
| Used (free-style = Total−Free−Buffers−Cached) | ~5,066,556 | |
| AnonPages | 1,079,604 | process anonymous memory, host-wide |
| ├─ attributable to visible container RSS | ~498,000 | sum of RSS of all 10 visible processes |
| └─ **hidden outside pid namespace** | ~580,000 | anon pages with no visible owner → host/other tenants (INFERENCE) |
| Slab | 316,272 | SReclaimable 189,152 / SUnreclaim 127,120 |
| Shmem (tmpfs) | 226,732 | already counted inside Cached — not double-counted |
| VmallocUsed | 60,000 | |
| Cached (page cache, reclaimable) | 1,871,688 | counts toward MemAvailable, not "used" |
| **Remainder of "used" (~3.3 GB)** | — | page tables, kernel stacks, and memory of processes outside this pid namespace — **not visible from inside** (FACT: meminfo is host-wide; no `memory.stat` exists) |

Cgroup check: neither `/sys/fs/cgroup/memory.stat` nor the v1 path exists —
no memory controller is attached, so per-cgroup accounting is UNAVAILABLE.

Top RSS: `hatch` (PID 67) 441 MB dominates; everything else < 12 MB.

## 3. Mount Summary

| Mount | Type / flags | Backing |
|-------|--------------|---------|
| `/` | overlay `rw,relatime` | upperdir=`/run/hatch/overlay/upper` (host-side); probe2's 2 GB write test proved **disk-backed** (MemAvailable never dropped) |
| `/home/hatch` | overlay `rw` **overmounted by** btrfs `/dev/mapper/rv` `rw,noatime,compress-force=zstd:3` | effective FS is btrfs, 100G — the durable area |
| `/tmp` | tmpfs `rw,nosuid,nodev` ×2 stacked (812M outer, **512M inner effective**) | RAM, ephemeral |
| `/var/tmp` | tmpfs `rw,nosuid,nodev`, 2G | RAM, ephemeral |
| `/sys` | tmpfs `ro` + sysfs `ro,nosuid,nodev,noexec` | read-only |
| `/opt/hatch`, `/etc/resolv.conf`, `/etc/hosts` | squashfs `ro` (bind mounts) | immutable |
| masked binaries (`messenger-cli`, `reboot-as-poweroff`, `wai`) | tmpfs overmount of `systemd/inaccessible/reg`, mode `----------` | blocked |
| ext4 | — | none present |

Namespace/capability boundary (unchanged from probe2):
`uid_map`/`gid_map` = `0 131072 65536` (root-in-userns); `capsh` Current =
everything except `cap_sys_ptrace`; `NoNewPrivs=1`.
