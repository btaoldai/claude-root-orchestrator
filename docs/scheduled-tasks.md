# Scheduled tasks — orchestration while nobody is watching

> Rule : ORCHESTRATEUR.md `<scheduled-tasks>`. Template : [`../prompts/scheduled-task.preprompt.md`](../prompts/scheduled-task.preprompt.md).

## Concept

A scheduled task is an orchestration started by a timer instead of a person : a nightly sprint, the preparation of a release, a weekly audit. Nobody reads along, nobody can answer a question, and the operator only sees what the run leaves behind (deliverables, a log, a notification). The doctrine turns those constraints into rules : the prompt must stand alone, the run must stop rather than guess, every deliverable must be audited by someone who did not write it, and every irreversible action is prepared for the operator instead of being made.

## What it does

### 1. A standalone pre-prompt

The stored prompt is the only context the run will have. It states :

- the **mission** in a few lines, and what is explicitly out of scope ;
- the **access** : which folder or repository, how to reach it, what to do if it is missing ;
- the **sources to read first, in order** (root instruction file, routing file, last two orchestrator logs, then the project files) ;
- the **deliverables**, each with its exact path ;
- the **absolute rules**, restated even if they are in `AGENT.md` : no git write, nothing deleted, no secret read or copied, LOCK files untouched, nothing published ;
- the **end** : a notification whose first sentence is the verdict.

### 2. Access check, then stop if needed

First action of the run : verify the workspace is reachable. If it is not, the run does nothing else, sends "workspace not attached, re-run after attaching it" and stops. A run that invents content to fill the gap is worse than a run that does nothing.

### 3. Read, replay, then work on a copy

The orchestrator reads the sources in order, replays the starting state (test suite, checks, counts) and writes it in its log. It works on a copy (sandbox, container, scratch clone) ; the workspace only receives finished deliverables.

### 4. Waves of experts with traces

Work is split into waves following the [supervised expert team](./paradigms.md) paradigm. Every brief ends with the mandatory-trace block (see [backlogs-and-traces.md](./backlogs-and-traces.md)) and carries a tool budget.

### 5. GO/NO-GO audits, second pass

Every deliverable is audited by a **fresh agent that did not write it**. It receives the artefact and the criteria, not the author's conclusions. Verdicts : GO, GO WITH CONDITIONS, NO-GO. Every refusal is corrected, then a second pass runs on the corrected version. A deliverable still NO-GO after the second correction is delivered as NO-GO, with its reasons ; it is never reported as done.

Typical auditors for a documentation release : a **leak auditor** (personal data, secrets, internal names ; checks by reading AND by grep with a written list of patterns) and a **coherence auditor** (a third-party reader understands it ; internal links resolve ; each document says what the thing is, what it does and what it does not do).

### 6. Delivery by archive or proposal folder

Deliverables land in a dated proposal folder (`00-control-center/_proposals/YYYY-MM-DD-{slug}/`), or in one archive extracted at the workspace root. Files are left writable by the operator. Temporary archives are moved to `_to-delete/` once extracted.

### 7. Logs, traces, handoff

- One orchestrator log per run : `.claude/logs/orchestrator/YYYY-MM-DD-HHMM-{slug}.md` (origin, access, waves table, verdicts, files touched, what is left).
- One trace per agent : `.claude/logs/agents/{role}/{project}/YYYY-MM-DD-HHMM-{slug}.md`, written by the orchestrator in relay when the agent could not write it. Closure gate : traces written = agents launched.
- Everything the run may not do is prepared for the operator : git commands in a runbook, LOCK changes as a diff, decisions with the reasons for and against and a recommendation.
- The run ends with a notification : verdict first, then the path of the deliverables and the operator's first action.

## What it does not do

- It does not publish, push, merge, tag or release anything : those are the operator's actions.
- It does not modify LOCK files : it proposes a diff in the proposal folder.
- It does not ask questions : it states its interpretation at the top of the log and proceeds, or stops when every path is irreversible.
- It does not replace the operator's review : a GO from an auditor means "ready for review", not "approved".

## Example orchestrator log (excerpt)

```markdown
---
date: YYYY-MM-DD
time: "HH:MM"
project: project-alpha
mission: sprint S<n> in autonomy (scheduled task)
status: delivered, audits GO, commits waiting for the operator
---
## Origin and access
Scheduled run. First firing : workspace not attached, stopped without doing anything.
Second firing : workspace reachable, sources read, starting state replayed (N tests green).

## Waves
| Wave | Agents | Result |
|---|---|---|
| S<n>.0 | architect (review), security (review) | two GO WITH CONDITIONS, conditions integrated |
| S<n>.1 | developer | N -> M tests, all checks green |
| S<n>.2 audits | qa-auditor, security-auditor (did not write the code) | major and minor findings listed |
| S<n>.2 fixes | developer | every finding fixed with tests ; second pass : GO |
| Closure | final-reviewer | GO, minor fixes applied |

## Traces (closure gate : N agents launched, N traces written)
- .claude/logs/agents/architect/project-alpha/YYYY-MM-DD-0845-review-adr-NNNN.md
- ...

## Left for the operator
Commits (commands in the sprint synthesis), decisions D-1 to D-n, phase update in ORCHESTRATEUR.md (LOCK, diff provided).
```
