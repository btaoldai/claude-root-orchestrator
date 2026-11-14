# Backlogs and traces

> Rules : AGENT.md `<universal-backlog-trace>` ; ORCHESTRATEUR.md `backlog-event-driven`, `backlogs-dual`, `agent-logs-format`.

## Concept

Two small files keep a multi-agent workspace recoverable without re-reading everything :

- the **claude-friendly backlog** (`.claude/backlogs/claude-friendly/backlog-{project}.md`) holds the current state of work items ; it is the single source of truth for "what is open" ;
- the **agent trace** (`.claude/logs/agents/{role}/{project}/YYYY-MM-DD-HHMM-{slug}.md`) records what one agent did in one mission.

The orchestrator rebuilds the state of a session from these files instead of asking every agent to read the full routing file.

## Claude-friendly backlog

### Format

```markdown
---
domain: project-alpha
updated: YYYY-MM-DDTHH:MM
priority_scale: P0-P3
status_values: [blocked, todo, in-progress, done]
---

# Backlog project-alpha

## P1 - Important

- id: PA-012
  task: Prepare release v1.4 of the documentation
  status: in-progress
  context: Scheduled run YYYY-MM-DD ; deliverables in _proposals/YYYY-MM-DD-docs-v1.4/ ; publication by the operator only.
  files: [00-control-center/_proposals/YYYY-MM-DD-docs-v1.4/]
```

### What it does

- One item = id, task, status, context (one or two lines), files.
- Written **on event only** : item done, long item started, new blocker. Target under 50 tokens per micro-write ; only systematic change : the `updated:` field.
- A status `todo` can sit on the operator's side : "publication by the operator, runbook at <path>".

### What it does not do

- No full rewrite outside explicit sprint planning.
- No prose : the optional human-friendly backlog exists for that, generated on demand.

## Agent trace

### Mandatory-trace block (paste at the end of every brief)

```xml
<mandatory-trace role="leak-auditor" path=".claude/logs/agents/leak-auditor/project-alpha/YYYY-MM-DD-HHMM-audit-leaks.md">
At the end of your mission, write this file (even if your mission is read-only) in the format
<session-id date agent model-tier model-id status> : mission, actions, modified files, status, 100 to 300 tokens.
If you cannot write it, end your report with this block filled in : the orchestrator will write it for you.
</mandatory-trace>
```

### Expected trace

```xml
<session-id date="YYYY-MM-DD-HHMM" agent="leak-auditor" model-tier="mid" model-id="actual-model-id" status="done" relay="orchestrator">
Mission : leak audit of the docs v1.4 tree (read + grep, written list of patterns).
Actions : read every changed file, grep pass 1 : 2 refusals (personal path in a code comment, unresolved placeholder) ; pass 2 after fixes : 0.
Files modified : none (read-only).
Status : GO.
</session-id>
```

`relay="orchestrator"` is present only when the orchestrator wrote the trace for the agent.

### Closure gate

The orchestrator log lists every agent launched with the path of its trace. A mission is not closed while traces written < agents launched ; a missing trace is reported to the operator.
