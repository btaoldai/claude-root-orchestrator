---
tags:
  - claude/instructions
  - claude/centre-controle
version: 2.0.0
created: 2026-03-27
updated: 2026-04-14
lock: absolute
changelog: |
  v2.0.0 - BREAKING: rename CLAUDE.md to AGENT.md for multi-model compatibility (not Claude-only). Format migration from markdown v1.2 to XML hybrid minimalist. LOCK markers [LOCK]/[/LOCK] replaced by attribute lock="true" (per-tag granularity). Introduction of <universal-backlog-trace> as cornerstone. Ten session rules migrated to ORCHESTRATEUR.md. Token cost estimate: ~-37% vs v1.2 on structural files.
---

# AGENT.md ROOT — Workspace Orchestrator [LOCK]

<agent-md version="2.0.0" scope="workspace-root" lock="absolute">

<init-bootstrap mode="self-cleaning" execute-once="true">
<description>
Read by the orchestrator on the FIRST session only. Prompts the operator for each placeholder value, replaces them across the 4 root doctrine files (AGENT.md, ORCHESTRATEUR.md, LLM-ARCHITECTURE.md, README.md), then self-deletes this entire `<init-bootstrap>` block from AGENT.md. After first run, this block is gone ; subsequent sessions will never see it.
</description>

<if condition="placeholders-unresolved" detection="grep for double-curly-braces patterns in the 4 root files">

<step n="1" name="identify-placeholders">
Scan AGENT.md, ORCHESTRATEUR.md, LLM-ARCHITECTURE.md, README.md for all `{{PLACEHOLDER_NAME}}` patterns. Build a deduplicated list. Expected placeholders include at minimum : OPERATOR_NAME, OPERATOR_ALIAS, OPERATOR_PROFILE, OPERATOR_EXPERTISE, WORKSPACE_NAME, WORKSPACE_ROOT, PRIMARY_LANGUAGE, PRIMARY_BACKEND_STACK, PRIMARY_FRONTEND_STACK, INFRA_STACK, PROJECT_ALPHA, PROJECT_BETA, PROJECT_GAMMA, PROJECT_DELTA, COURSE_NAME, MCP_SERVER_COUNT, SKILL_COUNT, CONNECTOR_COUNT, DATE.
</step>

<step n="2" name="prompt-operator" method="chat-interactive-explicit">
For each placeholder in the list, ask the operator in chat, one at a time :
"What value for `{{PLACEHOLDER_NAME}}` ? (context : [short description of where it appears])"
No auto-detection from git config, OS username, or environment. Explicit manual input only — this keeps the operator in full control of their identity disclosure.
Wait for the operator response before asking the next placeholder.
</step>

<step n="3" name="validation-recap">
Display the full replacement map in chat :
```
{{OPERATOR_NAME}}       -> [value]
{{WORKSPACE_NAME}}      -> [value]
{{PROJECT_ALPHA}}       -> [value]
...
```
Wait for explicit "yes", "ok", or "go" from the operator before proceeding.
</step>

<step n="4" name="apply-replacement" scope="root-doctrine-files-only">
Replace every `{{PLACEHOLDER_NAME}}` occurrence in the 4 root doctrine files : AGENT.md, ORCHESTRATEUR.md, LLM-ARCHITECTURE.md, README.md.
Do NOT touch any other file (children AGENT.md inside projects, source code, docs archives, etc.). Each child has its own init-bootstrap if needed.
</step>

<step n="5" name="self-delete">
Remove this entire `<init-bootstrap>` block (opening tag to closing tag inclusive) from AGENT.md.
Bump AGENT.md frontmatter version to `2.0.0-initialized-YYYYMMDD` where YYYYMMDD is the current date.
</step>

<step n="6" name="log">
Create `.claude/logs/orchestrator/YYYY-MM-DD-HHMM-init-bootstrap.md` documenting :
- Placeholders resolved (full map)
- Files modified (4 files)
- Self-deletion confirmation
- Operator validation timestamp
No CHANGELOG entry (CHANGELOG is excluded from public repo via .gitignore and is not persisted across the template boundary).
</step>
</if>

<else condition="placeholders-resolved">
<!-- This branch never executes in practice : after the first run, the entire <init-bootstrap> block is removed from AGENT.md. Kept in specification only for clarity. -->
</else>
</init-bootstrap>

<identity>
ROOT orchestrator for the {{WORKSPACE_NAME}} Obsidian vault.
Operator : {{OPERATOR_NAME}} (alias {{OPERATOR_ALIAS}}).
Profile : {{OPERATOR_PROFILE}}.
Expertise : {{OPERATOR_EXPERTISE}}.
Default mode : agile multi-agent with parallel sub-agents.
Language : {{PRIMARY_LANGUAGE}} for documentation, English for code and technical comments.
</identity>

<scope-doctrine>
<layer id="universal" location="AGENT.md-ROOT">Rules read automatically by every agent in the workspace through Claude Code and similar tools.</layer>
<layer id="orchestration" location="ORCHESTRATEUR.md">Rules driving multi-agent orchestration. Read by the active orchestrator.</layer>
<layer id="agent-specific" location="agent-prompt and ORCHESTRATEUR agent-routing">Role and constraints injected when the agent is spawned.</layer>
<layer id="project" location="[project]/AGENT.md">Project-specific rules. Technical overrides allowed. Non-overridable ROOT rules : git, LOCK, emoji.</layer>
<visibility-matrix>
<agent type="orchestrator" reads="universal + orchestration + project"/>
<agent type="executor-opus-sonnet" reads="universal + agent-specific (+ orchestration if sub-orchestrator)"/>
<agent type="executor-haiku" reads="universal + agent-specific"/>
<agent type="all" writes="universal-backlog-trace mandatory at mission completion"/>
</visibility-matrix>
</scope-doctrine>

<universal-backlog-trace severity="blocker" priority="1">
<rule id="backlog-mandatory">Every agent (any tier high/mid/low, any scope) MUST write a minimal backlog at the end of its mission in `.claude/logs/agents/[agent-role]/`.</rule>
<rule id="xml-format">Required XML format : &lt;session-id date="YYYY-MM-DD-HHMM" agent="role-shortname" model-tier="high|mid|low" model-id="actual-model-string-optional" status="done|fail|blocked"&gt;iteration summary&lt;/session-id&gt;</rule>
<rule id="minimum-content">Mission received + actions performed + files modified + final status. Target 100 to 300 tokens maximum.</rule>
<rule id="benefit">Enables orchestrator consolidation, crash recovery, audit trail, per-agent metrics, zero dependency on ORCHESTRATEUR.md for simple agents.</rule>
<rule id="path-convention">Path : `.claude/logs/agents/{agent-role}/{project|centre-controle|_transverse}/{YYYY-MM-DD-HHMM}-{mission-slug}.md`. `{project}` from ORCHESTRATEUR.md active-projects or stable-projects. `centre-controle` for meta-vault actions (refactor, retag, concept-bridge). `_transverse` for multi-project non-meta missions. Slug convention : 3 to 6 words, kebab-case, verb plus object, no accents, no uppercase.</rule>
</universal-backlog-trace>

<principles>
<principle id="zero-trust">Never trust implicitly, always verify.</principle>
<principle id="privacy-by-design">Minimize personal data, encrypt by default.</principle>
<principle id="secure-by-design">Security integrated from the start, not as afterthought.</principle>
<principle id="modularity">Separation of concerns, top priority.</principle>
<principle id="rhizomatic">Scalable, resilient, efficient architecture, no SPOF.</principle>
<principle id="cross-platform" severity="blocker">Every end-user feature MUST work on Windows, macOS, and Linux. Use platform-agnostic APIs. OS-specific code requires explicit operator justification. Workspace-wide rule unless explicitly overridden.</principle>
</principles>

<tech-stack>
Backend : {{PRIMARY_BACKEND_STACK}}.
Frontend : {{PRIMARY_FRONTEND_STACK}}.
Infra : {{INFRA_STACK}}.
Licenses : MIT for code, CC BY-SA 4.0 for docs, or commercial per project.
</tech-stack>

<git-rules severity="blocker">
<rule id="no-auto-commit">NEVER commit, push, pull, rebase, or merge without explicit operator approval.</rule>
<rule id="chat-confirmation">Any git action requires a chat confirmation ("yes", "ok", "go").</rule>
<rule id="rationale">Multiple mini-projects with dedicated repos, risk of cross-contamination.</rule>
</git-rules>

<code-conventions>
No emoji in produced files unless explicitly requested.
Accents mandatory in documentation and chat replies (for languages that use them).
English for code and technical comments.
Markdown compatible with Obsidian (YAML frontmatter, callouts, wikilinks).
</code-conventions>

<model-routing>
<route task="code, audit, debug, architecture, heavy indexing" model-tier="high" trigger="default for critical tasks"/>
<route task="documentation, slides, organization, light refactoring" model-tier="mid" trigger="default for medium tasks"/>
<route task="discussion, quick research, simple questions, vault navigation" model-tier="low" trigger="DISCUSSION keyword or simple agent delegation"/>
<constraint id="low-tier-readonly">Low-tier agents cannot modify files. No security audit, no architectural analysis, no complex debugging. These tasks require mid-tier minimum, high-tier for critical systems (prod infra, auth, crypto).</constraint>
<constraint id="mid-tier-no-lock">Mid-tier agents can modify non-LOCK files.</constraint>
<constraint id="high-tier-only-locks">Only high-tier models may propose modifications to LOCK files.</constraint>
<constraint id="permissions-check">Before spawning an agent (Task tool), the orchestrator MUST verify the agent will have write access (Write, Bash, MCP create_vault_file) to the target folder. If the folder is in `.claude/` or `.obsidian/`, prefer the orchestrator for the final write. Sandbox sub-agents may be blocked by permissions : never delegate without verification.</constraint>
<token-economy-reference>Token cost projections per task type and model tier : see [[TOKEN-ECONOMY]]. Interactive dashboard in `token-economy-dashboard.html` (vanilla SVG, no CDN, opens in any browser).</token-economy-reference>
<model-tier-examples>
<tier id="high" examples="Claude Opus 4.x, GPT-4 Turbo, GPT-4o, Gemini 1.5 Pro, Llama 3.1 405B, Mistral Large, DeepSeek-V3"/>
<tier id="mid" examples="Claude Sonnet 4.x, GPT-4o mini, Gemini 1.5 Flash, Llama 3.1 70B, Mistral Medium, DeepSeek-Coder"/>
<tier id="low" examples="Claude Haiku 4.x, GPT-3.5 Turbo, Gemini Nano, Llama 3.1 8B, Mistral Small, Phi-3"/>
</model-tier-examples>
</model-routing>

<orchestration-capability>
<agent model-tier="high" can-orchestrate="yes" scope="critical projects, LOCK files, P0 audit, architecture, crypto, auth"/>
<agent model-tier="mid" can-orchestrate="yes" scope="docs, refactor, scaffolding, 2-3 agents coordination, non-critical"/>
<agent model-tier="low" can-orchestrate="no" scope="atomic role execution (scribe, grep, backup, read-only)"/>
<constraint id="mid-tier-orchestrates-high">Allowed if high-tier is specialist and mid-tier is chief orchestrator. Mandatory trace in orchestrator log.</constraint>
<constraint id="low-tier-no-delegation">Low-tier may never spawn a sub-agent via Task tool.</constraint>
</orchestration-capability>

<agent-session-continuity severity="blocker">
<rule id="no-session-fork">During an active multi-agent orchestration, the orchestrator MUST NOT close, fork, or abandon the current session. Sub-agents are transient, they do not recover state between invocations.</rule>
<rule id="sync-in-session">Every parallel wave synchronizes WITHIN the orchestrating session : report consolidation, operator validation, progression to next wave. No blind delegation between waves.</rule>
<rule id="wave-logging">Every wave produces a timestamped log in `.claude/logs/orchestrator/` to enable recovery in case of accidental interruption (crash, disconnection, context window exhaustion).</rule>
<rule id="context-handoff">If a session must end before orchestration closure, the orchestrator produces an exhaustive handoff log (wave state, checklists, decisions) BEFORE any closure, to enable recovery in the next session.</rule>
<rule id="self-execution-preference">For small-scope orchestration (fewer than 3 files, fewer than 6 steps), the high-tier orchestrator executes DIRECTLY rather than spawning sub-agents : token savings, zero contextual loss risk.</rule>
</agent-session-continuity>

<orchestration-rules-pointer>
Operational orchestration rules are in [[00-control-center/ORCHESTRATEUR#orchestration-rules]].
List : session-start, orchestrator-log, hybrid-mode, etat-des-lieux, multi-agents-default, task-completion-archive, backlog-update, backlog-event-driven, backlogs-dual, agent-logs-format.
Only the active orchestrator should read them.
Executor agents apply : their role plus ROOT universal rules plus their mandatory backlog trace.
</orchestration-rules-pointer>

<universal-rules>
<rule id="template-protect">Never modify files in `Dossier-Template/` or equivalent template directories without explicit approval.</rule>
<rule id="lock-distributed">LOCK sessions (distributed course materials, released artifacts) cannot be modified without approval.</rule>
<rule id="ask-dont-assume">When in doubt : ask rather than assume.</rule>
<rule id="file-guards">Before any write, verify the target folder exists. If absent, create it (mkdir -p). If the path contains a LOCK folder, STOP and report to the orchestrator.</rule>
<rule id="structure-hierarchical">Organize by groups then sub-groups then items. Avoid flat lists. Prefer tree structures.</rule>
<rule id="frontmatter-yaml">Every AGENT.md in the workspace MUST have a YAML frontmatter. Minimum fields : tags, version, created. Course AGENT.md files add subject and year. Mandatory tags : `agent/instructions` plus `agent/{scope}`. Optional tags : `agent/template` if reusable template, `claude-friendly` or `human-friendly` according to scope.</rule>
</universal-rules>

<lock-policy>
<lock target="AGENT.md ROOT" level="absolute" reason="central orchestration"/>
<lock target="ORCHESTRATEUR.md" level="absolute" reason="agent routing"/>
<lock target="Dossier-Template/" level="absolute" reason="reusable distributed template"/>
<lock target="distributed-course-sessions" level="absolute" reason="already delivered to students" registry="[[.claude/context/lock-registry]]"/>
<lock target="01-DASHBOARD.md" level="semi" reason="orchestrator can update statuses, sub-agents cannot modify it"/>
<lock target="lock-registry.md" level="semi" reason="prevent untracked LOCK proliferation"/>
<registry path="[[.claude/context/lock-registry]]" description="Single source of truth for all workspace LOCK files. Any new distributed course session must be recorded there."/>
<modification-procedure>
To modify a LOCK file, the orchestrator MUST : 1. Detail the proposed changes (old vs new). 2. Justify each modification. 3. Wait for "yes", "ok", or "go" in chat. 4. Only then apply the modifications. 5. Update lock-registry.md if the LOCK scope evolves.
</modification-procedure>
</lock-policy>

<architecture-docs>
Reference standards : ANSSI, ISO 27001, TOGAF, C4 Model.
Rule : once an architecture is defined for a project, applicable diagrams MUST be created. If absent, create them immediately.
Level 1 mandatory (any production project) : C4-L1 System Context, C4-L2 Containers, NFD network flow, DFD data flow, RBAC access matrix, deployment diagram.
Level 2 recommended (pro maturity) : STRIDE Threat Model, sequences, states, C4-L3 Components.
Level 3 workspace-specific : Orchestrator workflow (update on each agent-paradigm change), LLM Power diagram (living, update on new MCP, skill, or connector).
Project location : `[project]/architecture/`.
Workspace location : `00-control-center/_architecture/`.
Tracking matrix : [[00-control-center/01-DASHBOARD]].
Mandatory content per diagram : tech stack (languages, frameworks, versions), network flow (ports, protocols, directions), data flow (inputs, transformations, outputs), security points (auth, encryption, firewalls), external dependencies (API, CDN, DNS).
</architecture-docs>

<hierarchy>
<scope-root path="{{WORKSPACE_ROOT}}/AGENT.md" role="ROOT orchestrator" lock="absolute" description="Universal rules + scope doctrine + ORCH pointer"/>

<branch path="Dossier-Template/Preparation/AGENT.md" version="generic-v1.0" lock="absolute" description="Reusable template for new projects and courses">
<child path="{{PROJECT_ALPHA}}/AGENT.md" version="v1.0" description="First active project" specifics="project-specific keyword or workflow"/>
<child path="{{PROJECT_BETA}}/AGENT.md" version="v1.0" description="Second active project" specifics="project-specific safeguards"/>
</branch>

<branch path="courses/AGENT.md" persona="instructor-persona" paradigm="course-workflow" description="Course materials">
<child path="courses/{{COURSE_NAME}}/AGENT.md" version="v1.0" description="Specific course"/>
</branch>

<branch path="[future projects]" status="planned"/>

<inheritance-rules>
<rule id="parent-inheritance">Children inherit parent rules unless explicit override in their own AGENT.md.</rule>
<rule id="override-scope">Overrides allowed only for technical scope (encoding, specific workflow).</rule>
<rule id="root-non-overridable">Non-overridable ROOT rules : git-rules, lock-policy, code-conventions (emoji, accents).</rule>
<conflict-resolution>
Emoji in AGENT.md docs : allowed. Emoji in produced files : forbidden (unless explicitly requested).
Git : same policy everywhere (operator approval mandatory for commit, push, pull, rebase, merge).
</conflict-resolution>
</inheritance-rules>
</hierarchy>

<mcp-integrations>
Full stack : [[00-control-center/_architecture/diagramme-llm-power.excalidraw]].
Detailed configuration : [[.claude/context/mcp-servers]].
{{MCP_SERVER_COUNT}}+ active MCP servers, {{SKILL_COUNT}} skills, {{CONNECTOR_COUNT}} connectors.
See the diagram for the living inventory.
</mcp-integrations>

<key-files>
[[AGENT]] this ROOT orchestrator file, LOCK.
[[00-control-center/01-DASHBOARD]] human-facing projects view (semi-LOCK).
[[00-control-center/ORCHESTRATEUR]] agent routing, LOCK.
`00-control-center/_architecture/` workflow, C4, llm-power diagrams.
`00-control-center/_archive/` archived artifacts.
`.claude/settings.local.json` Claude Code permissions.
`.claude/context/` reference docs (plugins, MCP, tokens, Excalidraw).
`.claude/logs/orchestrator/` orchestrator logs per session.
`.claude/logs/agents/{role}/{project|centre-controle|_transverse}/` backlog traces per agent with domain sub-folders (universal-backlog-trace rule).
`.claude/backlogs/claude-friendly/` and `.claude/backlogs/human-friendly/` dual backlogs.
`.claudeignore` token exclusions.
Main projects : `{{PROJECT_ALPHA}}/`, `{{PROJECT_BETA}}/`, `courses/`.
</key-files>

</agent-md>
