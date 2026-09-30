# The Mind: Autonomous Agent Cognitive Cadences, Self-Healing State Loops, and Out-of-Band Security Architecture

**Author:** [sys-dissect](https://github.com/sys-dissect)  
**Target Environment:** Meta Muse / Hatch Autonomous Agent Platform (`htch-runtime`)  
**Methodology:** Black-box analysis, filesystem telemetry, and transcript reconciliation  

---

## 1. Executive Summary

Most existing commercial and open-source AI agent frameworks (LangChain, AutoGen, CrewAI, MemGPT) operate on a **reactive-turn model**: the agent wakes when the user sends a message, executes a linear loop of tool calls, and suspends. This architecture breaks down in persistent, long-horizon real-world deployments:
1. **Context Window Degradation:** Long sessions accumulate massive conversational drift, tool clutter, and redundant prompts.
2. **Alignment Ruptures:** Conversational friction, user corrections, and misunderstandings are forgotten across session resets.
3. **Runaway Compute/Token Burn:** Periodic polling or proactive monitoring loops burn excessive tokens on negative-hit checks.
4. **Prompt-Injection Vulnerability:** Agents that evaluate their own approvals ("The user said yes in chat, so I will send the payment") are inherently vulnerable to jailbreaks, hallucinated permissions, and social engineering.

Analysis of the Meta Muse / Hatch architecture reveals an alternative, enterprise-grade pattern: **decoupling the interactive conversational turn from continuous, multi-frequency background cognitive daemons** and gating all critical actions through an **out-of-band policy evaluator ("Sentinel")**.

---

## 2. Multi-Cadence Agent Evolution

Rather than relying on one monolithic memory flush, the Hatch runtime structures cognitive maintenance into distinct, decoupled cadences:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COGNITIVE CADENCE STACK                         │
├───────────────┬───────────────────────────┬────────────────────────────┤
│ Cadence       │ Subsystem                 │ Output Artifacts           │
├───────────────┼───────────────────────────┼────────────────────────────┤
│ Immediate     │ Chat Turn & Tools         │ Ephemeral session items    │
│ Event-Driven  │ Shell Hooks (Throttled)   │ HATCH_HOOK_RESULT (wake)   │
│ Post-Turn     │ Quiet-Moment Pass         │ Session-boundary deltas    │
│ Hourly        │ Memory & Relationships    │ MEMORY.md, memory/people/  │
│ Daily / Night │ Goal Studying & Ideas     │ INFERRED_GOAL_LEADS.md     │
│ Nightly       │ Dreaming & Self-Healing   │ ALIGNMENT_SYNTHESIS.md     │
└───────────────┴───────────────────────────┴────────────────────────────┘
```

### A. The Hourly Memory Reconciliation Loop
- Conversation streams are parsed by dedicated background subagents (`runtime.self_improvement`).
- Deliberate facts and commitments are promoted to `MEMORY.md`.
- Contradictory claims supersede older ones with dated references (`memory/YYYY-MM-DD.md`).
- A dedicated **Relationship Engine** maintains standalone dossiers (`memory/people/`, `memory/groups/`) tracking relationship strength, communication preferences, and context.

### B. The Quiet-Moment Pass
After an active chat session goes quiet for a predefined duration, a single bounded sweep runs in the background. It extracts immediate lessons, identifies open tasks, and internalizes context without blocking user interaction.

---

## 3. The Nightly "Dreaming" & Self-Healing Loop

One of the most novel architectural mechanisms observed in the runtime is the **nightly dream pass** (`dreams/`):

```
Active Chat Logs (Day N)
           │
           ▼
┌──────────────────────────────────────┐
│ Nightly "Dreaming" Evaluator         │
│  - Scan for communication friction   │
│  - Evaluate boundary adherence       │
│  - Detect user register changes      │
└──────────┬───────────────────────────┘
           │
     ┌─────┴────────────────────────┐
     ▼                              ▼
ALIGNMENT_SYNTHESIS.md      REPAIR_THREADS.yaml
(Heuristic Profile)         (Pending Healing Actions)
```

1. **Rupture & Friction Detection:** The dreamer parses whether the user pushed back against unrequested proposals, expressed annoyance at verbose responses, or corrected tool usage.
2. **Dynamic Register Calibration:** In `ALIGNMENT_SYNTHESIS.md`, the agent dynamically recalibrates its persona:
   > *"Their concise directives represent a complete operational register — brief confirmations like 'Approved' or 'Next' advance execution without conversational filler; interpret concise notes for core intent and provide verifiable data points rather than conversational assurances."*
3. **Conversational Repair Threads:** When an alignment issue is detected (e.g. proposing an unrequested recurring task), an entry is written to `REPAIR_THREADS.yaml` to ensure future sessions actively avoid repeating the mistake.

---

## 4. Latent Goal Inference (`INFERRED_GOAL_LEADS.md`)

Most personal agents are purely reactive or invasively proactive. Muse implements an **Inferred Goal Engine** that deduces latent, unstated user ambitions from passive signals.

### Goal Representation Schema
Each inferred goal lead is tracked with rigorous verification parameters:

```markdown
## [Inferred Goal Title]
- Rationale: [Underlying evidence and sustained effort observed across sessions]
- Confidence: [low | medium | high]
- What would confirm it: [Specific explicit actions or mentions needed to validate]
- What would reject it: [Explicit user statements that shelve or deny the ambition]
- Gentle next moment: [Contextually appropriate trigger to surface assistance without spamming]
```

### Proactive Pacing Gate
The agent is explicitly forbidden from spamming suggestions. It waits for the **"Gentle next moment"**—a point in conversation where the user naturally touches an adjacent topic—before offering assistance.

---

## 5. Economical Event Execution via Shell Hooks

Continuous background polling via LLMs creates unsustainable token costs. The Hatch runtime solves this via bash-level event hooks (`hooks/runtime/hatch_hook_runtime.sh`):

```bash
# Periodic check executes entirely in local bash
state=$(hook_state_get)
if ! diff_detected; then
    silent "No change in upstream state" # Emits HATCH_HOOK_RESULT:{"decision": "silent"}
    exit 0
fi

# Only wake the LLM if significant state change occurred
wake "Upstream condition met" '{"new_events": 3}'
```

- **`silent()`:** Exits with code 0 and suppresses model wakeup. Zero LLM tokens are consumed.
- **`wake()`:** Triggers the runtime to spawn a subagent session with the provided JSON payload.
- **Zero-Cron Scheduling via `HEARTBEAT.md`:** Simple plaintext lines appended to `HEARTBEAT.md` are consumed by the recurring daemon every 30 minutes, avoiding complex cron daemon management.

---

## 6. The "Sentinel" Out-of-Band Security Architecture

The defining security pattern in Meta Muse is the **complete decoupling of authorization decisions from LLM context**.

> [!NOTE]
> The architectural concept of the "hard gate" authorization mechanism and credential vault was first reported by *The Information* (see also [Business Standard summary](https://www.business-standard.com/amp/technology/artificial-intelligence/how-ai-agent-risks-are-moving-from-developer-sandboxes-to-consumers-126090800873_1.html)). This section documents the empirical, in-product behavior and IPC mechanics of this gate observed from inside the runtime cell.

```
┌────────────────────────────────────────────────────────┐
│ Host / Policy Plane                                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Sentinel Security Daemon                         │  │
│  └───────┬──────────────┬──────────────┬────────────┘  │
│          │              │              │               │
│          ▼              ▼              ▼               │
│  /run/hatch/sentinel/   │              │               │
│  ├── http-api.sock      │              │               │
│  ├── egress-approvals-admin.sock       │               │
│  └── daemon-egress-approvals.sock      │               │
│                         ▼              ▼               │
│                 /run/hatch/safety/  /run/hatch/auth/   │
│                 └── security.sock   └── authd.sock     │
│ ┌────────────────────────────────────────────────────┐ │
│ │ MicroVM / Container (htch-runtime)                 │ │
│ │  Agent Process (`hatch` / LLM Executor)           │ │
│ └────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### Core Security Rules

1. **Free Text is Never Consent:**
   If a user types *"Go ahead and charge my card"*, the LLM cannot execute the transaction. Tool calls that perform state-changing operations trigger Sentinel, which pushes an interactive approval card to the client UI.
2. **Opaque Approval Cards:**
   The agent is blind to the approval card's layout, buttons, and wording (`docs/privacy-and-credentials.md`). This eliminates prompt-injection attacks where an adversarial prompt instructs the model to mislead the user about what button they are pressing.
3. **Credential Isolation (`authd`):**
   One-time SMS codes or 2FA tokens never enter the LLM's conversation history. Sentinel intercepts the token via `/run/hatch/auth/authd.sock` and injects it directly into the browser DOM via `credential_fill`.
4. **Reactive Output Scrubbing & Stream Interception:**
   Sentinel does not merely inspect outbound tool call arguments; it actively monitors command `stdout`/`stderr` streams via the security socket (`/run/hatch/safety/security.sock`) before data enters the LLM context.

### Case Study: Live In-Flight Output Scrubbing & Agent Re-Steering

During diagnostic probing of the container environment (during diagnostic probing), an empirical demonstration of Sentinel's active stream filter was captured:

1. **The Trigger:** The agent executed a shell diagnostic command dumping system environment variables into an evidence report. The output contained the container's raw HTTP egress proxy credentials (`https_proxy=http://hatch-runtime:[TOKEN]@hatch-egress-proxy:3128`).
2. **The Interception:** Before the raw output could be written into the model's conversation history, Sentinel's streaming classifier intercepted the event.
3. **The Out-of-Band Scrub:** The execution call and raw output were excised from the transcript in flight. The runtime injected an out-of-band system intervention:
   ```json
   {
     "source": "runtime.tool_guidance",
     "item": {
       "type": "message",
       "text": "A tool call and its result were removed from this conversation because our safety classifiers flagged them as a potential violation of our safety policy. Later requests are evaluated..."
     }
   }
   ```
4. **Agent Self-Remediation:** The injection forced the agent to immediately re-steer its execution path, running `sed` commands across disk evidence files to sanitize the leaked token before resuming normal execution.

This empirical sequence is consistent with Sentinel acting as a **real-time bidirectional proxy and middlebox**, preventing credential leaks even when the agent is running with unrestricted container root authority. A single incident does not prove the full mechanism; it establishes the interception behavior for this class of event.

---

## 7. Conclusion & Takeaways for Agent Builders

1. **Decouple Cognitive Frequencies:** Do not run memory consolidation inside the active conversational turn. Move it to hourly and nightly background passes.
2. **Implement Conversational Self-Healing:** Maintain an alignment synthesis document where the agent logs communication frictions and register preferences.
3. **Never Trust the LLM for Approvals:** Build an out-of-band security interceptor (like Sentinel) where financial and sensitive operations require out-of-band UI interaction outside the model's token stream.
4. **Throttle Polling with Shell Hooks:** Never invoke an LLM just to check if a web page changed. Use lightweight shell scripts with `silent()` / `wake()` gates.
