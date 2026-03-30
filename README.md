# Claude Root Orchestrator — Multi-Agent Template for Claude Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

A production-ready, reusable template for orchestrating complex software projects using Claude Code with a multi-agent architecture. Designed for developers and technical leads who want structured, auditable, and scalable AI-assisted development workflows.

---

## Overview

This template provides a complete CLAUDE.md-based orchestration system for Claude Code. It defines a hierarchy of instruction files, agent routing logic, model selection rules, and collaboration patterns that allow a single operator to coordinate multiple specialized AI agents across different projects within a single workspace.

The core insight is that Claude Code works best not as a single monolithic assistant, but as an orchestrator that delegates tasks to specialized sub-agents — each with the right model, the right context, and the right permissions for its scope.

---

## Architecture

### CLAUDE.md Hierarchy

The system relies on a cascading hierarchy of CLAUDE.md instruction files:

```
CLAUDE.md (ROOT — Orchestrator)              [scope: entire workspace]
  |
  +-- project-alpha/CLAUDE.md               [scope: project alpha only]
  |     Inherits ROOT rules, adds project-specific workflow
  |
  +-- project-beta/CLAUDE.md                [scope: project beta only]
  |     Inherits ROOT rules, adds project-specific workflow
  |     |
  |     +-- project-beta/sub-module/CLAUDE.md   [scope: sub-module]
  |
  +-- courses/CLAUDE.md                     [scope: course materials]
        Inherits ROOT rules, adds pedagogical constraints
```

**Inheritance rules:**
- Child CLAUDE.md files inherit all ROOT rules unless explicitly overriding
- Overrides are permitted only for technical scope (encoding, tooling, workflow)
- ROOT invariants (git policy, LOCK rules, emoji policy) cannot be overridden
- Any CLAUDE.md is a LOCK file — no agent may modify it without operator approval

### ORCHESTRATEUR.md — The Routing Table

A dedicated `ORCHESTRATEUR.md` file acts as the single source of truth for agent routing. It contains:

- The active project registry with current status
- Agent team definitions (personas, models, responsibilities)
- Session detection logic (which agent to activate based on user message)
- Cross-project dependency map

### Agent Model Selection

| Task Type | Model | Trigger |
|-----------|-------|---------|
| Code, security audit, architecture, heavy indexing | claude-opus-4-6 | Default for critical tasks |
| Documentation, slides, organization, light refactoring | claude-sonnet-4-6 | Default for medium tasks |
| Research, quick questions, vault navigation | claude-haiku-4-5 | Keyword DISCUSSION or simple delegation |

---

## LLM Collaboration Architecture

This template is designed for a multi-LLM workflow where different AI systems handle different parts of the development process based on their strengths.

```
                        +------------------+
                        |    OPERATOR      |
                        |  (human lead)    |
                        +--------+---------+
                                 |
           +---------------------+---------------------+
           |                     |                     |
  +--------v--------+   +--------v--------+   +--------v--------+
  | Claude Opus 4.6 |   | Claude Sonnet   |   | Claude Haiku    |
  | Code & Audit    |   | Docs & Refactor |   | Research & Nav  |
  | Architecture    |   | Slides & Org    |   | Quick lookups   |
  +-----------------+   +-----------------+   +-----------------+
                                 |
                        +--------v---------+
                        | Perplexity /     |
                        | Gemini           |
                        | Tech watch       |
                        | Web research     |
                        +------------------+
```

### Model Responsibilities

| LLM | Primary Role | Use When |
|-----|-------------|----------|
| Claude Opus 4.6 | Architecture decisions, security audits, complex debugging, production code | High-stakes code, infra changes, cryptography, auth systems |
| Claude Sonnet 4.6 | Documentation, refactoring, course materials, moderate code tasks | Non-critical files, writing tasks, reorganization |
| Claude Haiku 4.5 | Fast lookups, vault navigation, information retrieval | Read-only tasks, quick questions, agent delegation |
| Perplexity / Gemini | Technology watch, web research, up-to-date documentation lookup | External research, library version checking, CVE lookup |

### Collaboration Workflow Example

A typical feature development cycle using this multi-LLM system:

1. **Research phase** — Perplexity/Gemini: look up current best practices, check for relevant CVEs, find library documentation
2. **Architecture phase** — Claude Opus: design the system, write ADRs, define interfaces
3. **Implementation phase** — Claude Opus: write production code, implement security controls
4. **Documentation phase** — Claude Sonnet: write user-facing docs, inline comments, README updates
5. **Review phase** — Claude Opus: security audit, code review, performance analysis
6. **Communication phase** — Claude Sonnet: generate changelogs, slide decks, status reports

This pipeline ensures that each LLM operates within its optimal domain while the operator maintains control over all critical decisions.

---

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) installed and authenticated
- An Obsidian vault (or any directory-based workspace)
- Basic familiarity with CLAUDE.md instruction files

### Installation

1. Clone this repository into your workspace root:

```bash
git clone https://github.com/{{OPERATOR_ALIAS}}/claude-root-orchestrator .claude-template
```

2. Copy the template files to your workspace root:

```bash
cp .claude-template/CLAUDE.md ./CLAUDE.md
cp .claude-template/ORCHESTRATEUR.md ./00-control-center/ORCHESTRATEUR.md
```

3. Replace all placeholders with your own values:

| Placeholder | Replace with |
|-------------|-------------|
| `{{OPERATOR_NAME}}` | Your full name |
| `{{OPERATOR_ALIAS}}` | Your username or handle |
| `{{PROJECT_ALPHA}}` | Your first project name |
| `{{PROJECT_BETA}}` | Your second project name |
| `{{WORKSPACE_ROOT}}` | Absolute path to your workspace |

4. Create the required directory structure (see File Structure below).

5. Open Claude Code at your workspace root and start a new session. The orchestrator will read CLAUDE.md automatically.

### Adapting the Template

- **Add a project**: Create a `project-name/CLAUDE.md` inheriting from ROOT, then register it in `ORCHESTRATEUR.md`
- **Add an agent persona**: Define the persona in `ORCHESTRATEUR.md` with its model, scope, and triggers
- **Add a LOCK file**: Document it in CLAUDE.md section 10 and announce it in the session log
- **Change model routing**: Edit the model selection table in CLAUDE.md section 8

---

## File Structure

```
workspace-root/
  CLAUDE.md                              # ROOT orchestrator (this template)
  .gitignore                             # Obsidian + Claude Code exclusions
  00-control-center/
    01-DASHBOARD.md                      # Human-readable project overview (Semi-LOCK)
    ORCHESTRATEUR.md                     # Agent routing table (LOCK)
    _architecture/                       # Diagrams: workflow, C4, LLM architecture
    _archive/                            # Archived artefacts with date prefix
  .claude/
    settings.local.json                  # Claude Code permissions
    context/                             # Reference docs (plugins, MCP, tokens)
    logs/
      orchestrator/                      # Session logs (YYYY-MM-DD-HH:MM.md)
      agents/                            # Per-agent task logs
    backlogs/                            # claude-friendly + human-friendly backlogs
  project-alpha/
    CLAUDE.md                            # Project-specific instructions (child)
    NEXT-STEPS.md                        # Living roadmap for this project
    architecture/                        # C4, NFD, DFD, RBAC diagrams
  project-beta/
    CLAUDE.md
    NEXT-STEPS.md
    architecture/
  courses/
    CLAUDE.md                            # Course-specific constraints
    course-name/
      sessions/                          # Individual course sessions (LOCK when distributed)
```

---

## Key Concepts

### LOCK Files

Certain files are declared LOCK and cannot be modified by any agent without explicit operator approval. The operator must provide a verbal confirmation ("yes", "ok", "go") in chat before any modification is applied.

Default LOCK files in this template:
- `CLAUDE.md` (all levels of the hierarchy)
- `ORCHESTRATEUR.md`
- `Dossier-Template/` (template directories)
- Distributed course sessions

### Semi-LOCK Files

The `01-DASHBOARD.md` is Semi-LOCK: the orchestrator agent can update statuses and tick completed items, but individual sub-agents cannot modify it directly.

### Session Logging

Every session creates a log file at `.claude/logs/orchestrator/YYYY-MM-DD-HH:MM.md`. This provides an auditable trail of what was decided, what was delegated, and what was completed.

### Backlogs

Two parallel backlog formats are maintained in `.claude/backlogs/`:
- `claude-friendly`: structured for agent consumption (machine-readable, concise)
- `human-friendly`: structured for the operator (prose, context, priorities)

---

## Credits and Methodology

This orchestration system is grounded in the principles of structured AI collaboration as defined by Anthropic's AI Fluency Framework:

[Anthropic AI Fluency Framework — Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations)

Key methodological principles applied in this template:

- **Operator/User/Assistant distinction**: The CLAUDE.md hierarchy maps directly to the operator-level trust model
- **Prompt chaining**: Complex tasks are decomposed into sequential agent calls with explicit handoffs
- **Tool use and delegation**: Sub-agents are given only the permissions they need (principle of least privilege)
- **Agentic safety**: LOCK files, explicit confirmation gates, and audit logs prevent unintended autonomous modifications

### The "Code with Review" Method

This template applies the AI Fluency Framework through a concrete iterative methodology called
"Code with Review". Each development cycle proceeds through six stages:

1. **Intent Declaration** — The operateur formulates the objective in natural language. The
   orchestrateur (Claude Opus) decomposes it into sub-tasks and dispatches to specialized agents.

2. **Multi-Agent Execution** — Multiple agents work in parallel on distinct files (zero conflict).
   Each agent is assigned the optimal model for its task: Opus for critical code, Sonnet for
   documentation, Haiku for research and navigation.

3. **Automated Review** — On each agent completion, the orchestrateur consolidates results.
   Automated validation tools (`cargo test`, `cargo clippy --pedantic`, `cargo audit`, `cargo fmt`)
   serve as quality gates before any result is accepted.

4. **Human-in-the-Loop Validation** — The operateur validates all structural decisions. LOCK
   files are only modified with explicit approval. Git actions (commit, push, merge) are always
   operator-triggered — never autonomous.

5. **Cross-LLM Enrichment** — For exploratory research or technology watch, external LLMs
   (Perplexity with Gemini) complement Claude. Results are synthesized by the orchestrateur
   before integration into any artifact. External outputs are never committed raw.

6. **Documentation-as-Code** — Every decision is traced (ADR), every session logged, every
   backlog synchronized. Documentation lives with the code, not alongside it as an afterthought.

The four practical principles driving this method (derived from the AI Fluency Framework):

- **Practical**: every LLM interaction produces a concrete artifact (code, doc, diagram)
- **Efficient**: routing by optimal model (Opus is not used for a simple lookup)
- **Ethical**: full transparency on LLM usage, credits in commits, no hidden automation
- **Safe**: zero-trust by default, credentials never exposed, mandatory human validation

Full technical detail for this methodology is documented in
[`_architecture/templatebat/LLM-ARCHITECTURE.md`](./LLM-ARCHITECTURE.md).

---

## License

MIT License — see [LICENSE](./LICENSE) for details.
