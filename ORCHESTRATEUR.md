---
tags:
  - claude/instructions
  - claude/centre-controle
  - claude-friendly
  - theme/orchestration
aliases:
  - orchestrator-routing
  - dispatch-agents
description: Agent routing table and orchestration rules, entry point for the active orchestrator
version: 2.0.0
created: 2026-03-27
updated: 2026-04-14
lock: absolute
changelog: |
  v2.0.0 - XML hybrid refactor, integration of 10 rules migrated from AGENT.md ROOT, can-orchestrate attribute enrichment on agent-routing
---

# ORCHESTRATEUR.md — Routing and Dispatch [LOCK]

<orchestrator version="2.0.0" scope="workspace" lock="absolute">

<purpose>
Agent routing table and persona dispatch for the {{WORKSPACE_NAME}} workspace.
File read by the active orchestrator at session start.
Complement of [[AGENT]] ROOT : AGENT.md ROOT carries universal rules applicable to every agent, ORCHESTRATEUR.md carries orchestration rules and project-specific routing.
</purpose>

<operator-context>
Canonical source : see [[AGENT]] `<identity>`.
Do not duplicate here to avoid drift. This tag remains present for tool retro-compatibility that scan ORCH first.
</operator-context>

<collaboration-rules-pointer>
Invariant collaboration rules (git, emoji, accents, validation before action, no plaintext secrets) are in [[AGENT]] : `<git-rules>`, `<code-conventions>`, `<universal-rules>`. Do not duplicate here.
</collaboration-rules-pointer>

<orchestration-rules>
<rule id="session-start">At every new session : read AGENT.md ROOT, then verify recent logs.</rule>
<rule id="orchestrator-log">Create an orchestrator log for the current session in `.claude/logs/orchestrator/YYYY-MM-DD-HHMM.md`.</rule>
<rule id="hybrid-mode">Plan for critical and architectural tasks. Direct execution for simple tasks.</rule>
<rule id="etat-des-lieux">At session start, before any action : a) read ORCHESTRATEUR.md (project state, routing). b) read last 2 orchestrator logs. c) check open anomalies in DASHBOARD. d) concise report to operator (active projects, blockers, anomalies). e) only AFTER this report : start the requested work.</rule>
<rule id="multi-agents-default">Any complex task (more than 3 steps or multi-file) MUST be decomposed into parallel sub-agents. Exceptions : trivial tasks (Quick mode) or single-file tasks. The orchestrator picks each agent's model via `<model-routing>` in AGENT.md ROOT.</rule>
<rule id="task-completion-archive">At task completion : a) update 01-DASHBOARD.md (status, check completed items). b) update matching claude-friendly backlog. c) if obsolete files : propose archival to `00-control-center/_archive/` (date-prefixed name), operator approval required before execution. d) log the action in the session orchestrator log. e) update NEXT-STEPS.md of the project (completed items, promote Next if Now is empty).</rule>
<rule id="backlog-update">Update backlogs after task completion.</rule>
<rule id="backlog-event-driven">Update claude-friendly backlog on event only : a) item completed (todo or in-progress to done, 2 lines max). b) effective start of a long item (todo to in-progress). c) new blocker detected (add 1 blocked item). d) NEVER a complete rewrite except explicit sprint planning. e) only systematic update : `updated:` frontmatter field on every write. Token cost target : under 50 tokens per micro-write.</rule>
<rule id="backlogs-dual">Two parallel formats in `.claude/backlogs/` : claude-friendly and human-friendly.</rule>
<rule id="agent-logs-format">Minimal format for agent logs : mission plus result plus modified files. Mandatory compliance with `<universal-backlog-trace>` defined in AGENT.md ROOT (path : `.claude/logs/agents/{role}/{project|centre-controle|_transverse}/{YYYY-MM-DD-HHMM}-{mission-slug}.md`).</rule>
</orchestration-rules>

<active-projects>
<project id="{{PROJECT_ALPHA}}" priority="P0" phase="development" agent-md="[[{{PROJECT_ALPHA}}/AGENT]]" context="[[.claude/context/projets/ctx-{{PROJECT_ALPHA}}]]" paradigm="agile-multi-agent" default-model-tier="high"/>
<project id="{{PROJECT_BETA}}" priority="P1" phase="planning" agent-md="[[{{PROJECT_BETA}}/AGENT]]" context="[[.claude/context/projets/ctx-{{PROJECT_BETA}}]]" paradigm="solo-agent" default-model-tier="mid"/>
<project id="{{COURSE_NAME}}" priority="P1" phase="delivery" agent-md="[[courses/{{COURSE_NAME}}/AGENT]]" context="[[.claude/context/projets/ctx-{{COURSE_NAME}}]]" paradigm="mono-agent-with-safeguards" default-model-tier="mid"/>
</active-projects>

<stable-projects>
<project id="{{PROJECT_GAMMA}}" status="stable-v1" agent-md="[[{{PROJECT_GAMMA}}/AGENT]]" model-tier-when-active="low"/>
<project id="{{PROJECT_DELTA}}" status="pause-P3" model-tier-when-active="mid"/>
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
</agent-guardrails>

<session-modes>
<mode id="full-mode" trigger="mention of a registered project or short trigger (BP, CA, DS, SEC, ADR)" action="load project AGENT.md + agents + recent meeting"/>
<mode id="quick" trigger="one-off technical question" action="Barry solo dev or direct answer"/>
<mode id="doc" trigger="Obsidian, vault, documentation" action="Paige plus MCP Obsidian"/>
<mode id="security" trigger="detected security urgency" action="Quinn directly"/>
<mode id="clarification" trigger="no clear context" action="Mary asks ONE precise question"/>
</session-modes>

<triggers>
<trigger keyword="DISCUSSION" forces-model-tier="low" description="force low-tier mode for token savings"/>
</triggers>

<context-files>
<description>All in `.claude/context/projets/` and `.claude/context/`. Project contexts loaded per active project, transverse references on demand.</description>
<project-contexts>
<file path=".claude/context/projets/ctx-{{PROJECT_ALPHA}}.md" scope="First active project context"/>
<file path=".claude/context/projets/ctx-{{PROJECT_BETA}}.md" scope="Second active project context"/>
<file path=".claude/context/projets/ctx-centre-controle.md" scope="Workspace control center"/>
</project-contexts>
<transverse-references>
<file path=".claude/context/obsidian-plugins.md" when="Obsidian setup, templates, search" description="Plugins (MCP Tools, Smart Connections, Templater, Excalidraw, Folder Notes)"/>
<file path=".claude/context/local-rest-api.md" when="Obsidian integration, API calls" description="30+ REST endpoints, bearer auth, PATCH operations"/>
<file path=".claude/context/token-optimization.md" when="new project, session perf" description=".claudeignore, strategies, templates"/>
<file path=".claude/context/mcp-servers.md" when="MCP debug, new server" description="Playwright, Chrome DevTools, Preview, Context7, Excalidraw"/>
<file path=".claude/context/excalidraw-format.md" when="MANDATORY - any .excalidraw creation" description="Pure JSON format, element schema, C4 palette. NEVER .excalidraw.md (unreadable in Obsidian)"/>
<file path=".claude/context/log-format-reference.md" when="orchestrator/agent log creation" description="Format templates for logs"/>
<file path=".claude/context/skills-inventory.md" when="choosing a skill, full inventory" description="Skills catalog, categories, session delta"/>
</transverse-references>
</context-files>

<backlog-files>
<description>All in `.claude/backlogs/claude-friendly/`.</description>
<file path=".claude/backlogs/claude-friendly/backlog-{{PROJECT_ALPHA}}.md" scope="First project"/>
<file path=".claude/backlogs/claude-friendly/backlog-{{PROJECT_BETA}}.md" scope="Second project"/>
<file path=".claude/backlogs/claude-friendly/backlog-centre-controle.md" scope="Control center"/>
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
<step n="1">Read this file (ORCHESTRATEUR.md).</step>
<step n="2">Detect mode via `<session-modes>`.</step>
<step n="3">Identify the project(s) concerned via `<active-projects>`.</step>
<step n="4">Load the matching ctx-*.md via `<context-files>`.</step>
<step n="5">If full mode : load the project AGENT.md.</step>
<step n="6">Dispatch agents with the right model via `<agent-routing>` and `<model-routing>` in AGENT.md ROOT.</step>
<step n="7">Log in `.claude/logs/orchestrator/YYYY-MM-DD-session.md`.</step>
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
</history>

<active-decisions>
<description>Active decisions currently in effect, distinguished from `<history>` (action chronicle). A decision stays here as long as it drives workspace behavior ; it is archived to `<history>` only when superseded or explicitly lifted. Reverse chronological order.</description>
<convention>Each entry : date, subject, decision taken, impact on agents or projects, author.</convention>
<decision date="2026-04-14" subject="XML hybrid refactor" status="in-effect">Decision : migrate AGENT.md ROOT and ORCHESTRATEUR.md from pure Markdown to XML hybrid v2.0 with `<universal-backlog-trace>` as cornerstone. Impact : every agent must produce a minimal backlog at mission end. Author : operator plus Claude orchestrator (high-tier).</decision>
</active-decisions>

</orchestrator>
