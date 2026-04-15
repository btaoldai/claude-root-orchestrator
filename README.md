# Claude Root Orchestrator — Multi-Agent Template for AI Coding Assistants

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./CHANGELOG.md)

A production-ready, reusable template for orchestrating complex software projects using AI coding assistants (Claude Code, Cursor, Aider, and compatible tools) with a multi-agent architecture. Designed for developers and technical leads who want structured, auditable, and scalable AI-assisted development workflows.

---

## What's new in v2.0.0

**BREAKING CHANGES** from v1.x :

- `CLAUDE.md` renamed to **`AGENT.md`** for multi-model compatibility (works with Claude Code, but also other AI assistants that read instruction files).
- Format migrated from pure Markdown to **XML hybrid minimalist** : structure carried by self-descriptive XML tags, content preserved as markdown (paragraphs, wikilinks, code blocks).
- LOCK markers `[LOCK]` / `[/LOCK]` replaced by `lock="true"` XML attribute — granularity is now per-tag.
- Cornerstone tag `<universal-backlog-trace>` added : every agent, regardless of scope or model, leaves a minimal XML trace at mission end. The orchestrator reconstructs state from these traces rather than requiring all agents to re-read the full ORCHESTRATEUR.md.
- Ten session rules migrated from `AGENT.md` ROOT into `ORCHESTRATEUR.md` `<orchestration-rules>`. Only the active orchestrator needs to read them.
- Full English documentation (v1.x was partially French).

Token cost improvement : approximately **-37%** on structural files (AGENT.md ROOT) and **-16%** on ORCHESTRATEUR.md versus v1.2 markdown.

See [CHANGELOG.md](./CHANGELOG.md) for full detail.

---

## Zero-Config Setup via `<init-bootstrap>`

This v2 template ships with an **automatic initialization mechanism**. You don't have to hunt for placeholders or edit files manually.

On the first session after cloning, the orchestrator reads AGENT.md, detects the `<init-bootstrap>` block at the top, and walks you through setup :

1. **It identifies every `{{PLACEHOLDER}}` across the 4 root doctrine files** (AGENT.md, ORCHESTRATEUR.md, LLM-ARCHITECTURE.md, README.md).
2. **It asks you in chat, one placeholder at a time** : "What value for `{{OPERATOR_NAME}}` ?", "What value for `{{WORKSPACE_NAME}}` ?", etc. No git config scraping, no OS username sniffing — explicit manual input only, you stay in full control of what you disclose.
3. **It shows you the full replacement map** and waits for your explicit "yes", "ok", or "go".
4. **It applies all replacements** across the 4 files.
5. **It self-deletes the `<init-bootstrap>` block** from AGENT.md. Subsequent sessions will never see it again.
6. **It logs the operation** in `.claude/logs/orchestrator/YYYY-MM-DD-HHMM-init-bootstrap.md`.

Expected first-run pre-prompt flow :

```
You  : [open Claude Code in the cloned template folder, say anything]
Claude: I detected an uninitialized template (placeholders present in 4 files).
        I will walk you through setup step by step.
        First question : What value for `{{OPERATOR_NAME}}` ? (context : shown in AGENT.md identity and in LLM-ARCHITECTURE.md diagram)
You  : Alice
Claude: Got it. Next : What value for `{{OPERATOR_ALIAS}}` ? (context : used in README install example)
You  : alice-dev
... [repeats for each placeholder] ...
Claude: Here is the full replacement map :
        {{OPERATOR_NAME}}       -> Alice
        {{OPERATOR_ALIAS}}      -> alice-dev
        {{WORKSPACE_NAME}}      -> alice-vault
        {{PROJECT_ALPHA}}       -> solana-bot
        ...
        Proceed with replacements ?
You  : go
Claude: [applies replacements, removes <init-bootstrap>, bumps version, logs to .claude/logs/orchestrator/]
        Template initialized. The init-bootstrap is gone. Ready to work.
```

**Prefer manual setup?** Skip the automatic flow by manually editing the 4 root files with your values, then remove the `<init-bootstrap>` block yourself. Both paths lead to the same state.

---

## Overview

This template provides a complete **AGENT.md-based orchestration system** for AI coding assistants. It defines a hierarchy of instruction files, agent routing logic, model selection rules, and collaboration patterns that allow a single operator to coordinate multiple specialized AI agents across different projects within a single workspace.

The core insight is that AI coding assistants work best not as a single monolithic assistant, but as an orchestrator that delegates tasks to specialized sub-agents — each with the right model, the right context, and the right permissions for its scope.

---

## Architecture

### AGENT.md Hierarchy

The system relies on a cascading hierarchy of AGENT.md instruction files :

```
AGENT.md (ROOT — Orchestrator)                [scope: entire workspace]
  |
  +-- project-alpha/AGENT.md                  [scope: project alpha only]
  |     Inherits ROOT rules, adds project-specific workflow
  |
  +-- project-beta/AGENT.md                   [scope: project beta only]
  |     Inherits ROOT rules, adds project-specific workflow
  |     |
  |     +-- project-beta/sub-module/AGENT.md  [scope: sub-module]
  |
  +-- courses/AGENT.md                        [scope: course materials]
        Inherits ROOT rules, adds pedagogical constraints
```

**Inheritance rules :**

- Child AGENT.md files inherit all ROOT rules unless explicitly overriding.
- Overrides are permitted only for technical scope (encoding, tooling, workflow).
- ROOT invariants (git policy, LOCK rules, emoji policy) cannot be overridden.
- Any AGENT.md is a LOCK file — no agent may modify it without operator approval.

### ORCHESTRATEUR.md — The Routing Table

A dedicated `ORCHESTRATEUR.md` file acts as the single source of truth for agent routing. It contains :

- The active project registry with current status
- Stable / paused / archived projects
- Agent team definitions (personas, models, responsibilities, can-orchestrate flag)
- Session detection logic (which agent to activate based on user message)
- Orchestration rules (10 rules migrated from ROOT in v2)
- Active decisions (distinct from history — decisions currently driving behavior)

### Agent Model Selection (tier-based, multi-LLM)

The template is **model-agnostic**. Map your preferred LLMs to three tiers :

| Task Type | Model Tier | Trigger | Example models |
|-----------|-----------|---------|----------------|
| Code, security audit, architecture, heavy indexing | `high` | Default for critical tasks | Claude Opus, GPT-4 Turbo, GPT-4o, Gemini 1.5 Pro, Llama 3.1 405B, Mistral Large |
| Documentation, slides, organization, light refactoring | `mid` | Default for medium tasks | Claude Sonnet, GPT-4o mini, Gemini 1.5 Flash, Llama 3.1 70B, Mistral Medium |
| Research, quick questions, vault navigation | `low` | Keyword DISCUSSION or simple delegation | Claude Haiku, GPT-3.5 Turbo, Gemini Nano, Llama 3.1 8B, Mistral Small |

In `AGENT.md` and `ORCHESTRATEUR.md`, model selection uses the `model-tier="high|mid|low"` attribute so you can swap your actual provider without touching the doctrine.

### Token economy

For detailed token consumption projections by task type and model tier, see [`TOKEN-ECONOMY.md`](./TOKEN-ECONOMY.md). An interactive SVG dashboard is available at [`token-economy-dashboard.html`](./token-economy-dashboard.html) — open it in any browser locally, no CDN or server required (vanilla SVG + vanilla JS in a single self-contained file).

---

## LLM Collaboration Architecture

This template is designed for a multi-LLM workflow where different AI systems handle different parts of the development process based on their strengths. See [LLM-ARCHITECTURE.md](./LLM-ARCHITECTURE.md) for full detail (now in XML hybrid v2).

---

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) (or a compatible AI coding assistant that reads AGENT.md) installed and authenticated
- An Obsidian vault (or any directory-based workspace)
- Basic familiarity with AGENT.md-style instruction files

### Installation

1. Clone this repository into your workspace root :

```bash
git clone https://github.com/btaoldai/claude-root-orchestrator .agent-template
```

2. Copy the template files to your workspace root :

```bash
cp .agent-template/AGENT.md ./AGENT.md
cp .agent-template/ORCHESTRATEUR.md ./00-control-center/ORCHESTRATEUR.md
cp .agent-template/LLM-ARCHITECTURE.md ./00-control-center/_architecture/LLM-ARCHITECTURE.md
```

3. Replace all placeholders with your own values :

| Placeholder | Replace with |
|-------------|--------------|
| `{{OPERATOR_NAME}}` | Your full name |
| `{{OPERATOR_ALIAS}}` | Your username or handle |
| `{{OPERATOR_PROFILE}}` | Short profile (e.g., "Cybersecurity instructor and independent developer") |
| `{{OPERATOR_EXPERTISE}}` | Expertise areas (e.g., "Rust, DevOps, infosec") |
| `{{WORKSPACE_NAME}}` | Your workspace name |
| `{{WORKSPACE_ROOT}}` | Absolute path to your workspace |
| `{{PRIMARY_LANGUAGE}}` | Your preferred documentation language (English, French, etc.) |
| `{{PRIMARY_BACKEND_STACK}}` | Your primary backend tech |
| `{{PRIMARY_FRONTEND_STACK}}` | Your primary frontend tech |
| `{{INFRA_STACK}}` | Your infra tech |
| `{{PROJECT_ALPHA}}` | Your first active project name |
| `{{PROJECT_BETA}}` | Your second active project name |
| `{{PROJECT_GAMMA}}`, `{{PROJECT_DELTA}}` | Stable projects |
| `{{COURSE_NAME}}` | A course name if applicable |
| `{{MCP_SERVER_COUNT}}`, `{{SKILL_COUNT}}`, `{{CONNECTOR_COUNT}}` | Your MCP inventory counts |
| `{{DATE}}` | Current date (in LLM-ARCHITECTURE.md) |

4. Create the required directory structure (see File Structure below).

5. Open Claude Code (or your AI assistant) at your workspace root and start a new session. The orchestrator will read AGENT.md automatically.

### Adapting the Template

- **Add a project** : create a `project-name/AGENT.md` inheriting from ROOT, then register it in `ORCHESTRATEUR.md` `<active-projects>`.
- **Add an agent persona** : define the persona in `ORCHESTRATEUR.md` `<agent-routing>` with its model, triggers, description, and `can-orchestrate` flag.
- **Add a LOCK file** : register it in `AGENT.md` `<lock-policy>` and log the addition in the session orchestrator log. Update `.claude/context/lock-registry.md` for the central registry.
- **Change model routing** : edit the `<model-routing>` table in AGENT.md ROOT.

---

## File Structure

```
workspace-root/
  AGENT.md                               # ROOT orchestrator (this template)
  .gitignore                             # Obsidian + Claude Code exclusions
  00-control-center/
    01-DASHBOARD.md                      # Human-readable project overview (semi-LOCK)
    ORCHESTRATEUR.md                     # Agent routing table (LOCK)
    _architecture/                       # Diagrams: workflow, C4, LLM architecture
      LLM-ARCHITECTURE.md                # Multi-LLM methodology (XML hybrid v2)
    _archive/                            # Archived artifacts with date prefix
  .claude/
    settings.local.json                  # Claude Code permissions
    context/                             # Reference docs
      lock-registry.md                   # Central registry of LOCK files
    logs/
      orchestrator/                      # Session logs (YYYY-MM-DD-HHMM.md)
      agents/                            # Per-agent task logs
        {role}/
          {project|centre-controle|_transverse}/
            YYYY-MM-DD-HHMM-mission-slug.md
    backlogs/                            # claude-friendly + human-friendly backlogs
  project-alpha/
    AGENT.md                             # Project-specific instructions (child)
    NEXT-STEPS.md                        # Living roadmap for this project
    architecture/                        # C4, NFD, DFD, RBAC diagrams
  project-beta/
    AGENT.md
    NEXT-STEPS.md
    architecture/
  courses/
    AGENT.md                             # Course-specific constraints
    course-name/
      sessions/                          # Individual course sessions (LOCK when distributed)
```

---

## Key Concepts

### LOCK Files

Certain files are declared LOCK and cannot be modified by any agent without explicit operator approval. The operator must provide a verbal confirmation ("yes", "ok", "go") in chat before any modification is applied.

Default LOCK files in this template :

- `AGENT.md` (all levels of the hierarchy)
- `ORCHESTRATEUR.md`
- `Dossier-Template/` (template directories)
- Distributed course sessions (tracked in `.claude/context/lock-registry.md`)

### Semi-LOCK Files

The `01-DASHBOARD.md` is semi-LOCK : the orchestrator agent can update statuses and tick completed items, but individual sub-agents cannot modify it directly.

### Universal Backlog Trace (v2 cornerstone)

Every agent spawned in a session, regardless of its model tier (high, mid, low) or scope, MUST produce a minimal XML backlog entry at mission end. This enables :

- The orchestrator to consolidate state without requiring all agents to read the full ORCHESTRATEUR.md (token savings).
- Crash recovery and session handoff.
- Audit trail and per-agent metrics.

Path convention : `.claude/logs/agents/{role}/{project|centre-controle|_transverse}/{YYYY-MM-DD-HHMM}-{mission-slug}.md`.

### Session Logging

Every session creates a log file at `.claude/logs/orchestrator/YYYY-MM-DD-HHMM.md`. This provides an auditable trail of what was decided, what was delegated, and what was completed.

### Dual Backlogs

Two parallel backlog formats are maintained in `.claude/backlogs/` :

- `claude-friendly/` : structured for agent consumption (machine-readable, concise, event-driven micro-writes of under 50 tokens).
- `human-friendly/` : structured for the operator (prose, context, priorities).

---

## Credits and Methodology

This orchestration system is grounded in the principles of structured AI collaboration as defined by Anthropic's AI Fluency Framework :

[Anthropic AI Fluency Framework — Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations)

Key methodological principles applied in this template :

- **Operator/User/Assistant distinction** — the AGENT.md hierarchy maps directly to the operator-level trust model.
- **Prompt chaining** — complex tasks are decomposed into sequential agent calls with explicit handoffs.
- **Tool use and delegation** — sub-agents are given only the permissions they need (principle of least privilege).
- **Agentic safety** — LOCK files, explicit confirmation gates, and audit logs prevent unintended autonomous modifications.
- **Universal traceability (v2)** — the `<universal-backlog-trace>` requirement enables post-hoc reconstruction of multi-agent sessions without requiring full context sharing.

### The "Code with Review" Method

This template applies the AI Fluency Framework through a concrete iterative methodology called **"Code with Review"**. Each development cycle proceeds through six stages, documented in detail in [`LLM-ARCHITECTURE.md`](./LLM-ARCHITECTURE.md) section `<development-workflow>` :

1. **Research** — external LLMs (Perplexity, Gemini) gather current best practices, CVEs, library docs.
2. **Architecture** — a high-tier model designs the system, produces ADRs and diagrams.
3. **Implementation** — a high-tier model writes production code, unit tests, integration.
4. **Documentation** — a mid-tier model writes README, inline docs, changelog, slides.
5. **Security Review** — a high-tier model audits the code, threat model, RBAC validation.
6. **Operator Validation** — the human operator validates all structural decisions and triggers git actions (commit, push, merge) — never autonomous.

The four practical principles driving this method (derived from the AI Fluency Framework) :

- **Practical** — every LLM interaction produces a concrete artifact (code, doc, diagram).
- **Efficient** — routing by optimal model tier (high-tier is not used for a simple lookup).
- **Ethical** — full transparency on LLM usage, credits in commits, no hidden automation.
- **Safe** — zero-trust by default, credentials never exposed, mandatory human validation.

---

## License

MIT License — see [LICENSE](./LICENSE) for details.
