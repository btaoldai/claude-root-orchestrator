---
tags:
  - claude/instructions
  - claude/control-center
  - claude-friendly
  - theme/orchestration
aliases:
  - orchestrator-routing
  - dispatch-agents
description: Agent routing table and orchestration rules, entry point for the active orchestrator
version: 2.3.0
created: 2026-03-27
updated: 2026-11-12
lock: absolute
changelog: |
  v2.3.0 - Project table grouped by theme with explicit phases; project-table, git-delegation, nothing-deleted and lock-diff rules; trace template for sub-agent briefs; paradigms (supervised expert team, independent GO/NO-GO gates); scheduled-tasks doctrine; token-economy rules; repo-hygiene pointer.
  v2.0.0 - XML hybrid refactor, integration of 10 rules migrated from AGENT.md ROOT, can-orchestrate attribute enrichment on agent-routing
---

# ORCHESTRATEUR.md — Routing and Dispatch [LOCK]

<orchestrator version="2.3.0" scope="workspace" lock="absolute">

<purpose>
Agent routing table and persona dispatch for the {{WORKSPACE_NAME}} workspace.
File read by the active orchestrator at session start.
Complement of [[AGENT]] ROOT : AGENT.md ROOT carries universal rules applicable to every agent, ORCHESTRATEUR.md carries orchestration rules and project-specific routing.
Map of this file (read the block you need, not the whole file) : orchestration-rules, themes, active-projects, stable-projects, agent-routing, paradigms, loop-cycle, scribe-rules, agent-guardrails, scheduled-tasks, token-economy, session-modes, context-files, backlog-files, semantic-scan, workflow-session, next-steps-protocol, history, active-decisions.
</purpose>

<operator-context>
Canonical source : see [[AGENT]] `<identity>`.
Operator environment (permanent variables, shell aliases, SSH host aliases) : `.claude/context/operator-env.md`, names and roles only, never a host name, an IP address or a secret. Read it before writing a command the operator will run ; never assume those aliases exist in the agent's own shell.
Do not duplicate here to avoid drift. This tag remains present for tool retro-compatibility that scan ORCH first.
</operator-context>

<collaboration-rules-pointer>
Invariant collaboration rules (git, emoji, accents, validation before action, no plaintext secrets) are in [[AGENT]] : `<git-rules>`, `<code-conventions>`, `<universal-rules>`. Do not duplicate here.
</collaboration-rules-pointer>

<orchestration-rules>
<rule id="session-start">At every new session : read AGENT.md ROOT, then verify recent logs.</rule>
<rule id="orchestrator-log">Create an orchestrator log for the current session in `.claude/logs/orchestrator/YYYY-MM-DD-HHMM-{slug}.md`.</rule>
<rule id="hybrid-mode">Plan for critical and architectural tasks. Direct execution for simple tasks.</rule>
<rule id="etat-des-lieux">At session start, before any action : a) read ORCHESTRATEUR.md (project state, routing). b) read the last 2 orchestrator logs. c) check open anomalies in DASHBOARD. d) apply the project-table rule. e) concise report to operator (active projects, blockers, anomalies, table gaps). f) only AFTER this report : start the requested work.</rule>
<rule id="project-table" severity="blocker">At session start, the orchestrator reconciles `<active-projects>` and `<stable-projects>` with the workspace, ideally with a read-only script (for example `scripts/check-project-table.py`, to write for your layout) that reports : project folders with no entry, entries whose instruction file path is dead, projects with recent logs but a stale phase. Every gap is presented to the operator as a registration card plus a diff (rule project-new of AGENT.md ROOT). After "go", the orchestrator edits ORCHESTRATEUR.md (version bump, changelog line) and re-runs the check : zero gap expected. Never a silent correction, never by a sub-agent.</rule>
<rule id="lock-diff" severity="blocker">Applying an approved change to a LOCK file : a) keep the current version as `_history/{file}.v{old-version}` ; b) re-check that the file did not change since the diff was computed (fingerprint, for example the first 16 hex characters of its SHA-256) ; if it changed, recompute the diff and ask again ; c) apply ; d) bump version and changelog in the same write. A diff prepared by a scheduled task waits in a proposal folder for the operator's go.</rule>
<rule id="multi-agents-default">Any complex task (more than 3 steps or multi-file) MUST be decomposed into parallel sub-agents. Exceptions : trivial tasks (Quick mode) or single-file tasks, and the self-execution-preference rule of AGENT.md ROOT. The orchestrator picks each agent's model via `<model-routing>` in AGENT.md ROOT.</rule>
<rule id="task-completion-archive">At task completion : a) update 01-DASHBOARD.md (status, check completed items). b) update matching claude-friendly backlog. c) if obsolete files : propose archival to `00-control-center/_archive/` (date-prefixed name), operator approval required before execution. d) log the action in the session orchestrator log. e) update NEXT-STEPS.md of the project (completed items, promote Next if Now is empty).</rule>
<rule id="nothing-deleted" severity="blocker">Agents never delete a file. What looks obsolete is moved (never copied) to one of four destinations : stays active ; `_history/` (previous version of something that was rewritten) ; `_archives/` (abandoned lead, dated snapshots in `_archives/backups/`) ; `_to-delete/YYYY-MM-DD/` (the operator deletes it himself, after review). Take a dated snapshot before any heavy clean-up pass.</rule>
<rule id="backlog-update">Update backlogs after task completion.</rule>
<rule id="backlog-event-driven">Update claude-friendly backlog on event only : a) item completed (todo or in-progress to done, 2 lines max). b) effective start of a long item (todo to in-progress). c) new blocker detected (add 1 blocked item). d) NEVER a complete rewrite except explicit sprint planning. e) only systematic update : `updated:` frontmatter field on every write. Token cost target : under 50 tokens per micro-write. Item format : see `docs/backlogs-and-traces.md`.</rule>
<rule id="backlogs-dual" priority="recommended">Two formats in `.claude/backlogs/` : claude-friendly (mandatory, single source of truth) and human-friendly (optional, generated on demand for projects where a prose view helps the operator). Do not maintain a human-friendly copy nobody reads.</rule>
<rule id="agent-logs-format">Minimal format for agent logs : mission plus result plus modified files. Mandatory compliance with `<universal-backlog-trace>` defined in AGENT.md ROOT (path : `.claude/logs/agents/{role}/{project|control-center|_transverse}/{YYYY-MM-DD-HHMM}-{mission-slug}.md`), brief-trace, orchestrator-relay and closure-gate rules included. Template to paste at the end of every sub-agent brief : &lt;mandatory-trace role="{role}" path=".claude/logs/agents/{role}/{project}/{YYYY-MM-DD-HHMM}-{slug}.md"&gt;At the end of your mission, write this file (even if your mission is read-only) in the format &lt;session-id date agent model-tier model-id status&gt; : mission, actions, modified files, status, 100 to 300 tokens. If you cannot write it, end your report with this block filled in : the orchestrator will write it for you.&lt;/mandatory-trace&gt;</rule>
<rule id="git-delegation" severity="blocker">No delegated agent (sub-agent, background agent, scheduled run) runs git or gh in write mode. A brief never asks for a commit, a push or a merge. An agent that needs a git action writes the exact command in its trace (repository, command, status blocked) ; the orchestrator groups those commands at the end of the wave and presents them to the operator, who runs them himself. A refusal from the tool layer is never worked around (no `git -C`, `sh -c`, script or alias).</rule>
</orchestration-rules>

<themes>
<description>Projects are grouped by theme so the table stays readable past a dozen entries. Rename, add or remove themes freely ; keep the `theme` attribute of each project in sync.</description>
<theme id="infra" description="servers, deployment, network, backups"/>
<theme id="teaching" description="courses, training sessions, grading"/>
<theme id="knowledge" description="wikis, knowledge bases, research notebooks"/>
<theme id="local-ai" description="local models, agents, assistants"/>
<theme id="dev-tools" description="CLIs, MCP servers, scripts, editor tooling"/>
<theme id="business" description="company, legal, accounting"/>
<theme id="personal" description="self-learning and side projects"/>
<phase-conventions>
Free text, but prefer one of these shapes so a script can parse it : `G{n}-{state}` for gate-driven projects (G0 framing to G8 delivery, state = open | green | in-progress) ; `S{n}-{state}` for sprint-driven projects ; `D-prod` / `D-prod-maintenance` for deployed services ; `framing`, `doc`, `self-learning` for small projects. A phase says where the project IS, not where it should be.
</phase-conventions>
</themes>

<active-projects>
<!-- theme: infra -->
<project id="{{PROJECT_ALPHA}}" theme="infra" priority="P0" phase="G3-green-G4-open" agent-md="[[{{PROJECT_ALPHA}}/AGENT]]" context="[[.claude/context/projects/ctx-{{PROJECT_ALPHA}}]]" paradigm="independent-go-nogo-gates" default-model-tier="mid" escalation-model-tier="high" notes="Plan : {{PROJECT_ALPHA}}/ROADMAP.md (gates G0-G8)."/>
<!-- theme: knowledge -->
<project id="{{PROJECT_BETA}}" theme="knowledge" priority="P1" phase="S2-in-progress" agent-md="[[{{PROJECT_BETA}}/AGENT]]" context="[[.claude/context/projects/ctx-{{PROJECT_BETA}}]]" paradigm="supervised-expert-team" default-model-tier="mid" escalation-model-tier="high"/>
<!-- theme: teaching -->
<project id="{{COURSE_NAME}}" theme="teaching" priority="P1" phase="delivery" agent-md="[[courses/{{COURSE_NAME}}/AGENT]]" context="[[.claude/context/projects/ctx-{{COURSE_NAME}}]]" paradigm="mono-agent-with-safeguards" default-model-tier="mid"/>
<!-- theme: dev-tools -->
<project id="example-small-tool" theme="dev-tools" priority="P3" phase="framing" agent-md="to-create" context="to-create" paradigm="solo-dev" default-model-tier="mid" notes="Registered by the project-table check ; replace or delete."/>
</active-projects>

<stable-projects>
<project id="{{PROJECT_GAMMA}}" status="stable-v1" agent-md="[[{{PROJECT_GAMMA}}/AGENT]]" model-tier-when-active="low"/>
<project id="{{PROJECT_DELTA}}" status="pause-P3" model-tier-when-active="mid"/>
<project id="example-abandoned" status="abandoned-YYYY-MM-DD" notes="Tombstone : keep the entry so the project-table check does not report the folder as unknown, until the folder itself is archived."/>
</stable-projects>

<agent-routing>
<agent name="mary" role="analyst" triggers="BP, RS, CB" model-tier="mid" can-orchestrate="no" description="briefing, requirements, clarification"/>
<agent name="john" role="product-manager" triggers="CP, VP, EP, US" model-tier="mid" can-orchestrate="no" description="specs, user stories"/>
<agent name="bob" role="scrum-master" triggers="SP, CS, PR" model-tier="low" can-orchestrate="no" description="planning, sprints"/>
<agent name="winston" role="architect" triggers="CA, IR, SA, ADR" model-tier="high" can-orchestrate="yes" description="technical decisions, ADRs"/>
<agent name="amelia" role="developer" triggers="DS, CR, RF" model-tier="mid" can-orchestrate="no" description="implementation, diffs"/>
<agent name="barry" role="solo-dev" triggers="QS, QD, QF" model-tier="low" can-orchestrate="no" description="quick fix, one-off script"/>
<agent name="dexter" role="devsecops" triggers="CICD, PIPE, SCAN, DEP, HARD" model-tier="high" can-orchestrate="yes" description="CI/CD pipeline, SAST/DAST scans, deps, secrets, hardening"/>
<agent name="quinn" role="qa" triggers="QA, TC, TB, ST" model-tier="mid" can-orchestrate="no" description="functional, integration, regression tests"/>
<agent name="sam" role="security-auditor" triggers="SEC, PEN, STRIDE, AUDIT" model-tier="high" can-orchestrate="yes" description="pen test, STRIDE, threat model, post-deployment audit"/>
<agent name="scribe" role="backlog-tracker" triggers="BL, LOG" model-tier="low" can-orchestrate="no" description="event-driven micro-write, loop traceability"/>
<agent name="paige" role="technical-writer" triggers="DP, WD, RD" model-tier="mid" can-orchestrate="no" description="docs, README, runbooks"/>
</agent-routing>

<paradigms>
<description>How a project is run. A project declares one or more paradigms in its `paradigm` attribute ; they can be combined. Details and examples : `docs/paradigms.md`.</description>
<paradigm id="solo-dev" description="One human, personas are hats worn by the orchestrator, AI sub-agents allowed, validation 100 % by the operator."/>
<paradigm id="mono-agent-with-safeguards" description="One agent at a time, domain guards (quality gates) applied before delivery."/>
<paradigm id="supervised-expert-team" description="Who does the work : expert agents (developer, auditor, fact-checker, analyst) launched in waves, each with a role, a tool budget and a mandatory trace ; the orchestrator re-checks every delivery (re-runs tests and checks) before writing anything to the workspace, and corrects, relaunches or asks the operator until the result holds. Never decides for the operator, never publishes, never runs git in write mode."/>
<paradigm id="independent-go-nogo-gates" description="When a step is closed : the project moves gate by gate, without a calendar ; each gate has exit criteria fixed in advance (pre-mortem at opening) and closes on the verdict GO, GO WITH CONDITIONS or NO-GO of an expert who did not produce the work. Counter-audit until GO ; the next gate opens as soon as the previous one is green."/>
</paradigms>

<loop-cycle>
<description>DevSecOps virtuous loop `/loop` : code then scan then test then fix then re-scan then re-test then PASS then audit then deploy.</description>
<flow>
Amelia (code) -> Dexter (SAST scan + deps + secrets + Dockerfile) -> Quinn (functional + integration tests) -> FAIL ? back to Amelia (fix) -> re-Dexter -> re-Quinn. 5th consecutive FAIL : Scribe creates a blocked item with cumulative context of the 5 failures. PASS : Sam security audit if critical project, then Deploy. Scribe updates done backlog. Paige updates doc if API or interface changed.
</flow>
<rule id="iteration-logging">Every iteration is logged in the agent log.</rule>
<rule id="fail-handling">On FAIL : log reason, Amelia adjusts, automatic retry.</rule>
<rule id="five-fail-blocker">On 5 consecutive FAIL : Scribe creates a blocked item in the claude-friendly backlog with cumulative context (reasons, files, attempted strategies).</rule>
<rule id="success-logging">On PASS and final SUCCESS : Scribe updates claude-friendly backlog (done item, result summary, modified files).</rule>
<rule id="sam-required-p0">Sam intervenes mandatorily if project is P0 or internet-facing.</rule>
<rule id="sam-optional-p2">Sam optional for P2+ (on request or if Dexter detects high risk).</rule>
<rule id="paige-api-change">Paige intervenes at end of loop if API or interface has changed.</rule>
</loop-cycle>

<scribe-rules>
<rule id="scribe-low-tier">Scribe is a low-tier model (minimalist writing, token savings).</rule>
<rule id="scribe-scope">Scribe modifies ONLY claude-friendly backlogs (`.claude/backlogs/claude-friendly/`).</rule>
<rule id="scribe-micro-write">Scribe respects `backlog-event-driven` : under 50 tokens per entry.</rule>
<rule id="scribe-auto">Scribe is triggered automatically by the `/loop`, no manual invocation needed.</rule>
<rule id="scribe-manual">Scribe can also be invoked manually via BL or LOG triggers for punctual backlog updates.</rule>
<rule id="scribe-frontmatter">Scribe updates the `updated:` frontmatter field on every write.</rule>
</scribe-rules>

<agent-guardrails>
<rule id="low-tier-readonly-exceptions">Complement to `low-tier-readonly` (AGENT.md ROOT `<model-routing>`). Allowed exceptions : Scribe writes only to `.claude/backlogs/claude-friendly/`. Bob writes only sprint planning files. No other exception without operator approval.</rule>
<rule id="mid-tier-non-lock">Mid-tier : can modify non-LOCK files.</rule>
<rule id="high-tier-lock">High-tier : only tier allowed to propose modifications on LOCK files.</rule>
<rule id="background-permissions">Before spawning a background agent : verify write rights on the target folder.</rule>
<rule id="claude-obsidian-orchestrator">If folder is in `.claude/` or `.obsidian/` : orchestrator writes, not the sub-agent.</rule>
<rule id="auditor-independence">An agent never audits what it produced. The audit that closes a step is run by a fresh agent that receives the artefact, not the author's conclusions.</rule>
</agent-guardrails>

<scheduled-tasks>
<description>A scheduled task is an orchestration that runs while nobody is watching (nightly sprint, release preparation, audit). The doctrine below makes it safe to run unattended. Details, pre-prompt template and example log : `docs/scheduled-tasks.md`, `prompts/scheduled-task.preprompt.md`.</description>
<rule id="standalone-preprompt">The stored prompt is complete and standalone : mission, sources to read first (in order), deliverables with their exact paths, absolute rules restated (no git write, nothing deleted, no secret, LOCK untouched, nothing published), end-of-run notification.</rule>
<rule id="access-check-first">First action : check that the workspace is reachable. If not, do nothing, notify "workspace not attached, re-run after attaching it" and stop. Never invent content to fill the gap.</rule>
<rule id="read-before-write">Read AGENT.md ROOT, ORCHESTRATEUR.md and the last two orchestrator logs before any production ; replay the starting state (tests, checks) and record it.</rule>
<rule id="working-copy">Work on a copy (sandbox or container), never directly on the workspace files ; the workspace receives only finished deliverables.</rule>
<rule id="team-and-waves">Waves of expert agents per the supervised-expert-team paradigm ; every brief carries the mandatory-trace block ; tool budget per agent (AGENT.md ROOT agent-budget).</rule>
<rule id="go-nogo-audit">Every deliverable is audited by an agent that did not write it (verdict GO, GO WITH CONDITIONS, NO-GO). Every refusal is corrected, then a second pass runs on the corrected version, until GO. A step still NO-GO after the second correction is delivered as NO-GO with its reasons, never silently as done.</rule>
<rule id="delivery-by-archive">Deliverables land in a dated proposal folder (`00-control-center/_proposals/YYYY-MM-DD-{slug}/`) or are extracted from one archive at the workspace root, files left writable by the operator. Temporary archives go to `_to-delete/` afterwards.</rule>
<rule id="logs-and-traces">One orchestrator log per run (`.claude/logs/orchestrator/YYYY-MM-DD-HHMM-{slug}.md` : origin, access, waves, verdicts, files touched, what is left for the operator) ; one trace per agent (`.claude/logs/agents/{role}/{project}/`), written by the orchestrator in relay when the agent could not write it. Closure gate : traces written = agents launched.</rule>
<rule id="operator-handoff">Everything the run may not do (git commands, LOCK changes, publication, deletions, decisions) is prepared as exact commands or diffs and listed for the operator, with the first action to take. The run ends with a notification whose first sentence is the verdict.</rule>
</scheduled-tasks>

<token-economy>
<rule id="read-the-map-first">Read the map of a long file (headings, block list) and then only the block needed. Grep targeted paths before opening a whole file.</rule>
<rule id="one-context-per-agent">Inject only the project context the agent needs ; an agent working on one project never receives the others.</rule>
<rule id="backlog-is-state">Use the claude-friendly backlog for current state instead of re-reading history or long logs.</rule>
<rule id="self-execute-small">Small scope (fewer than 3 files, fewer than 6 steps) : execute directly instead of spawning agents.</rule>
<rule id="no-oversized-injection">Never inject a result over 10K tokens into an agent context : give the path, let the agent read on demand.</rule>
<rule id="economy-by-default">Economy mode by default (mid-tier first) ; high-tier for multi-wave orchestration, critical audits and non-decomposable refactors. Projections : [[TOKEN-ECONOMY]].</rule>
</token-economy>

<session-modes>
<mode id="full-mode" trigger="mention of a registered project or short trigger (BP, CA, DS, SEC, ADR)" action="load project AGENT.md + agents + recent meeting"/>
<mode id="quick" trigger="one-off technical question" action="Barry solo dev or direct answer"/>
<mode id="doc" trigger="Obsidian, vault, documentation" action="Paige plus MCP Obsidian"/>
<mode id="security" trigger="detected security urgency" action="Quinn directly"/>
<mode id="clarification" trigger="no clear context" action="Mary asks ONE precise question"/>
<mode id="scheduled" trigger="run started by a schedule, nobody watching" action="apply `<scheduled-tasks>` ; reasonable interpretation stated at the top of the log instead of a question"/>
</session-modes>

<triggers>
<trigger keyword="DISCUSSION" forces-model-tier="low" description="force low-tier mode for token savings"/>
</triggers>

<context-files>
<description>All in `.claude/context/projects/` and `.claude/context/`. Project contexts loaded per active project, transverse references on demand.</description>
<project-contexts>
<file path=".claude/context/projects/ctx-{{PROJECT_ALPHA}}.md" scope="First active project context"/>
<file path=".claude/context/projects/ctx-{{PROJECT_BETA}}.md" scope="Second active project context"/>
<file path=".claude/context/projects/ctx-control-center.md" scope="Workspace control center"/>
</project-contexts>
<transverse-references>
<file path=".claude/context/operator-env.md" when="before writing a command the operator will run" description="Names and roles of permanent variables and aliases, never values"/>
<file path=".claude/context/obsidian-plugins.md" when="Obsidian setup, templates, search" description="Plugins (MCP Tools, Smart Connections, Templater, Excalidraw, Folder Notes)"/>
<file path=".claude/context/local-rest-api.md" when="Obsidian integration, API calls" description="30+ REST endpoints, bearer auth, PATCH operations"/>
<file path=".claude/context/token-optimization.md" when="new project, session perf" description=".claudeignore, strategies, templates"/>
<file path=".claude/context/mcp-servers.md" when="MCP debug, new server" description="Playwright, Chrome DevTools, Preview, Context7, Excalidraw"/>
<file path=".claude/context/excalidraw-format.md" when="MANDATORY - any .excalidraw creation" description="Pure JSON format, element schema, C4 palette. NEVER .excalidraw.md (unreadable in Obsidian)"/>
<file path=".claude/context/log-format-reference.md" when="orchestrator/agent log creation" description="Format templates for logs"/>
<file path=".claude/context/skills-inventory.md" when="choosing a skill, full inventory" description="Skills catalog, categories, session delta"/>
<file path="docs/repo-hygiene.md" when="creating or publishing a repository" description="Two levers : file template and repository settings"/>
</transverse-references>
</context-files>

<backlog-files>
<description>All in `.claude/backlogs/claude-friendly/`.</description>
<file path=".claude/backlogs/claude-friendly/backlog-{{PROJECT_ALPHA}}.md" scope="First project"/>
<file path=".claude/backlogs/claude-friendly/backlog-{{PROJECT_BETA}}.md" scope="Second project"/>
<file path=".claude/backlogs/claude-friendly/backlog-control-center.md" scope="Control center"/>
<file path=".claude/backlogs/claude-friendly/backlog-open-source.md" scope="Public GitHub repos"/>
</backlog-files>

<semantic-scan>
<priority>Hard paths (context-files) take priority. Semantic scan is a COMPLEMENT, not a replacement.</priority>
<decision-tree>
Request with known file or folder : direct Glob or Read via hard paths, NEVER semantic scan for structural queries.
Request with vague or transverse content : search_vault_smart (limit=5), score above 0.88 = reliable, inject max 3 results.
Precise keyword in a broad domain : Grep first (fast, exact). If too much noise (over 20 results) : semantic fallback.
Exploration or discovery : search_vault_smart (limit=5).
</decision-tree>
<anti-waste-rule>If hard paths or backlogs answer directly, do NOT run a semantic scan.</anti-waste-rule>
<workflow>
1. Identify the project via hard paths.
2. Load the matching ctx-*.md.
3. If additional context needed : apply the decision tree.
4. Do not inject more than 3 semantic results into agent context.
5. If a semantic result exceeds 10K tokens : do not inject it, note the path and let the agent read on demand.
</workflow>
<agent-instructions>
1. Receive the relevant ctx-*.md in the prompt.
2. Load the project AGENT.md if details are needed.
3. NEVER modify an AGENT.md without operator approval.
4. Log work in `.claude/logs/agents/` (universal-backlog-trace compliance).
</agent-instructions>
</semantic-scan>

<workflow-session>
<step n="1">Read this file (ORCHESTRATEUR.md), starting with the map in `<purpose>`.</step>
<step n="2">Detect mode via `<session-modes>`.</step>
<step n="3">Identify the project(s) concerned via `<active-projects>`.</step>
<step n="4">Load the matching ctx-*.md via `<context-files>`.</step>
<step n="5">If full mode : load the project AGENT.md.</step>
<step n="6">Dispatch agents with the right model via `<agent-routing>` and `<model-routing>` in AGENT.md ROOT, each brief ending with the mandatory-trace block.</step>
<step n="7">Log in `.claude/logs/orchestrator/YYYY-MM-DD-HHMM-{slug}.md`.</step>
<step n="8">Announce the active agent and the phase.</step>
</workflow-session>

<next-steps-protocol>
<purpose>Reduce cognitive load at task start. Each active project MUST have a NEXT-STEPS.md in its root folder.</purpose>
<format>
<section name="Now" required="yes">Atomic actions with exact commands, estimated time.</section>
<section name="Next" required="yes">Next batch of actions.</section>
<section name="Blocked or Waiting" required="if-applicable">Operator decisions or external deps.</section>
<section name="Quick context" required="yes">Wikilinks to backlog, AGENT.md, MOC, last log.</section>
</format>
<maintenance-rules>
1. The orchestrator updates NEXT-STEPS.md at every task end (task-completion-archive rule).
2. If a "Now" step is completed : move to Done or remove.
3. If "Now" is empty : promote items from "Next".
4. The DASHBOARD "Immediate actions" section is synchronized with active NEXT-STEPS.
5. Each step = ONE atomic action (not "configure everything").
6. Exact commands in code blocks (ssh, docker, cargo, etc.).
7. Estimated time per section, not per step (too granular).
</maintenance-rules>
<lifecycle>
Claude-friendly backlog (source of truth) -> NEXT-STEPS.md (action guide) -> Execution (operator) -> Backlog update (orchestrator).
</lifecycle>
</next-steps-protocol>

<history>
<entry date="2026-03-27" action="Creation of control center (audit and routing refactor)" author="Claude orchestrator plus operator"/>
<entry date="2026-04-14" action="XML hybrid refactor v2.0.0 : migration of 10 rules from AGENT.md ROOT to orchestration-rules, can-orchestrate enrichment on agent-routing, introduction of purpose, loop-cycle, scribe-rules, agent-guardrails tags" author="Claude orchestrator (high-tier) plus operator"/>
<entry date="2026-11-12" action="v2.3.0 : themes and phases, project-table, lock-diff, nothing-deleted, git-delegation, paradigms, scheduled-tasks, token-economy" author="Claude orchestrator (high-tier) plus operator"/>
</history>

<active-decisions>
<description>Active decisions currently in effect, distinguished from `<history>` (action chronicle). A decision stays here as long as it drives workspace behavior ; it is archived to `<history>` only when superseded or explicitly lifted. Reverse chronological order.</description>
<convention>Each entry : date, subject, decision taken, impact on agents or projects, author.</convention>
<decision date="2026-11-12" subject="Agents prepare git, the operator runs it" status="in-effect">Decision : no agent runs git or gh in write mode, even after a chat approval ; it prepares the exact command and the operator runs it. Impact : briefs never ask for commits ; scheduled runs end with a list of commands for the operator. Author : operator plus Claude orchestrator (high-tier).</decision>
<decision date="2026-04-14" subject="XML hybrid refactor" status="in-effect">Decision : migrate AGENT.md ROOT and ORCHESTRATEUR.md from pure Markdown to XML hybrid v2.0 with `<universal-backlog-trace>` as cornerstone. Impact : every agent must produce a minimal backlog at mission end. Author : operator plus Claude orchestrator (high-tier).</decision>
</active-decisions>

</orchestrator>
