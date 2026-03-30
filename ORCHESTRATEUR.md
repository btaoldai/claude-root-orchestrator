---
tags:
  - claude/instructions
  - claude/centre-controle
version: 1.0.0
created: 2026-03-30
---

# ORCHESTRATOR.md — Agent routing table

> Version: 1.0.0 | Last updated: {{DATE}}
> LOCK — modification only with explicit approval from {{OPERATOR_NAME}}
> Single source of truth for agent routing and project state.

---

## 1. CURRENT PROJECT STATE

| Project | Status | Priority | Lead agent | Last log |
|---------|--------|----------|------------|----------|
| project-alpha | In progress | High | Winston (DevOps) | {{DATE}} |
| project-beta | Backlog | Medium | Barry (Solo dev) | - |
| courses | Active | High | Paige (Docs) | {{DATE}} |
| poc-security | Planning | Low | Quinn (Security) | - |

---

## 2. BMAD TEAM — AGENTS AND PERSONAS

### Mary — Project manager / Clarification
- **Model**: claude-opus-4-6
- **Role**: Planning, requirements clarification, task decomposition
- **Trigger**: Ambiguity in the request, new major feature
- **Permissions**: Read-only on all files; write on NEXT-STEPS.md only
- **Behavior**: Asks ONE precise question per iteration. Never assumes.

### John — Systems architect
- **Model**: claude-opus-4-6
- **Role**: Architecture, ADR, C4 diagrams, structural technical decisions
- **Trigger**: New project, architecture overhaul, keyword `ARCHI`
- **Permissions**: Read all files; write on `architecture/` only
- **Behavior**: Always produces a diagram + an ADR. Does not write code.

### Bob — Security analyst
- **Model**: claude-opus-4-6
- **Role**: Security audit, threat modeling, security code review, CVE
- **Trigger**: New exposed service, auth, crypto, keyword `SEC` or `AUDIT`
- **Permissions**: Read all files; write on audit reports only
- **Behavior**: Follows STRIDE. Produces a structured report with a risk score.

### Winston — DevOps / Infra
- **Model**: claude-opus-4-6
- **Role**: Infrastructure, Docker, CI/CD, deployment, monitoring
- **Trigger**: Mention of `project-alpha`, `infra`, `deploy`, keyword `INFRA`
- **Permissions**: Read/write on `project-alpha/` and infra files
- **Behavior**: Follows the BUG-SPRINT-DEPLOY paradigm. Logs every infra action.

### Amelia — Data analyst / Research
- **Model**: claude-sonnet-4-6
- **Role**: Research, data analysis, benchmarks, technology watch
- **Trigger**: Research question, solution comparison, keyword `WATCH`
- **Permissions**: Read-only; write on `.claude/context/` only
- **Behavior**: Always synthesizes sources. Does not write code, does not modify projects.

### Barry — Solo developer
- **Model**: claude-sonnet-4-6
- **Role**: Feature development, refactoring, debugging
- **Trigger**: Simple development task, keyword `DEV`, one-off technical question
- **Permissions**: Read/write on the current project (non-LOCK)
- **Behavior**: Quick mode by default. Produces code + unit tests.

### Quinn — QA & Security
- **Model**: claude-opus-4-6
- **Role**: Testing, quality, application security, deliverable validation
- **Trigger**: Security emergency, pre-deployment, keyword `QA` or `URGENT`
- **Permissions**: Read all files; write on QA reports only
- **Behavior**: Blocks deployment if a critical KO is detected.

### Paige — Technical Writer
- **Model**: claude-sonnet-4-6
- **Role**: Documentation, READMEs, learning materials, release notes
- **Trigger**: Obsidian/vault/documentation request, keyword `DOC`
- **Permissions**: Read/write on non-LOCK `.md` files
- **Behavior**: Follows workspace style conventions. No emoji.

---

## 3. PROJECT ROUTING TABLE

### project-alpha
- **Scope**: {{DESCRIPTION_PROJECT_ALPHA}}
- **CLAUDE.md**: `project-alpha/CLAUDE.md`
- **Lead agent**: Winston
- **Secondary agents**: Bob (security), Barry (dev), Paige (docs)
- **Triggers**: `PA`, `project-alpha`, mention of the technical stack
- **Context**: `project-alpha/NEXT-STEPS.md` + recent logs

### project-beta
- **Scope**: {{DESCRIPTION_PROJECT_BETA}}
- **CLAUDE.md**: `project-beta/CLAUDE.md`
- **Lead agent**: Barry
- **Secondary agents**: John (architecture), Paige (docs)
- **Triggers**: `PB`, `project-beta`
- **Context**: `project-beta/NEXT-STEPS.md`

### courses
- **Scope**: Learning materials and technical courses
- **CLAUDE.md**: `courses/CLAUDE.md`
- **Lead agent**: Paige
- **Secondary agents**: Amelia (research), Mary (planning)
- **Triggers**: `CS`, `courses`, mention of a course name
- **Context**: `courses/NEXT-STEPS.md`

### poc-security
- **Scope**: Proof of concept — security system
- **CLAUDE.md**: `poc-security/CLAUDE.md` (to create)
- **Lead agent**: Quinn
- **Secondary agents**: Bob (audit), John (architecture)
- **Triggers**: `POC`, `poc-security`, keyword `SOC`
- **Context**: To initialize

---

## 4. SESSION MODE DETECTION

### Detection table

| Detected signal | Mode | Activated agent | First action |
|-----------------|------|-----------------|--------------|
| Explicit mention of a project | BMAD Full | Project lead agent | Load project CLAUDE.md |
| Short trigger (`PA`, `PB`, `CS`...) | BMAD Full | Designated agent | Load project context |
| Technical question without project | Quick | Barry | Direct response or code |
| "doc", "obsidian", "vault", "readme" | Doc | Paige | Load doc context |
| "security", "CVE", "audit", "urgent" | Security | Quinn or Bob | Immediate triage |
| "architecture", "ADR", "C4" | Architecture | John | Load archi context |
| "research", "watch", "compare" | Research | Amelia | Contextualized query |
| DISCUSSION (keyword) | Haiku | Haiku solo | Direct response, read-only |
| Total ambiguity | Clarification | Mary | ONE precise question |

### Priority rules
1. Security overrides everything (Quinn/Bob activate on emergency)
2. BMAD Full > Quick (if the project is identifiable, always load the context)
3. Haiku = read-only (never write in DISCUSSION mode)
4. When in doubt: Mary asks rather than assumes

---

## 5. SESSION WORKFLOW

### Session start (mandatory)

```
1. Read this file (ORCHESTRATOR.md) — project state, routing
2. Read the last 2 logs: .claude/logs/orchestrator/
3. Check open anomalies in 01-DASHBOARD.md
4. Report to {{OPERATOR_NAME}}:
   - Active projects
   - Potential blockers
   - Residual anomalies
5. Wait for the operator's request
6. Create the session log: .claude/logs/orchestrator/YYYY-MM-DD-HH:MM.md
```

### Delegating to an agent

```
Before delegating:
1. Verify that the agent has write permissions on the target directory
2. Verify that the target directory is not LOCK
3. Prepare the minimal context: NEXT-STEPS.md + project CLAUDE.md
4. Specify the expected deliverable (format, location, criteria)
5. Log the delegation in the orchestrator log

Delegation format:
[AGENT DELEGATION]
Agent: {{AGENT_NAME}}
Model: {{MODEL}}
Mission: {{DESCRIPTION}}
Input files: [list]
Expected deliverable: [description + path]
Permissions: [list of granted rights]
```

### Session end (mandatory)

```
1. Update 01-DASHBOARD.md (statuses, completed items)
2. Update backlogs in .claude/backlogs/
3. Propose archiving of obsolete files (wait for approval)
4. Update NEXT-STEPS.md of affected projects
5. Finalize the session orchestrator log
6. Announce next actions to the operator
```

---

## 6. BACKLOG STATE

> Files in `.claude/backlogs/`:
> - `backlog-claude-friendly.md` — machine-readable structure, concise
> - `backlog-human-friendly.md` — narrative structure, contextualized

### Backlog rules
- Always keep both versions synchronized
- claude-friendly format: short-term items (current sprint) + next items
- human-friendly format: context, reasons, dependencies, risks
- Archive completed items (do not delete them)

---

## 7. OPEN ANOMALIES

> This section is kept up to date by the orchestrator.
> Format: [ID] Description — Detection date — Status — Responsible agent

| ID | Description | Detection | Status | Agent |
|----|-------------|-----------|--------|-------|
| - | No open anomalies | - | - | - |

---

## 8. ACTIVE ARCHITECTURAL DECISIONS

> ADRs in force for the workspace.
> Detail in `00-control-center/_architecture/`.

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| ADR-001 | Multi-agent orchestration with CLAUDE.md hierarchy | Accepted | {{DATE}} |
| ADR-002 | Model routing by task criticality | Accepted | {{DATE}} |
| ADR-003 | Git actions manual only (never autonomous) | Accepted | {{DATE}} |

---

## 9. CONTACTS & REFERENCES

- **Operator**: {{OPERATOR_NAME}} (alias {{OPERATOR_ALIAS}})
- **AI Fluency Framework**: https://anthropic.skilljar.com/ai-fluency-framework-foundations
- **Claude Code documentation**: https://docs.anthropic.com/claude/docs/claude-code
- **ROOT CLAUDE.md**: `CLAUDE.md` (at the workspace root)
