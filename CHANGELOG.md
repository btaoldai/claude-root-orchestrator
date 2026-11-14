# Changelog

All notable changes to the claude-root-orchestrator template are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] — 2026-11-12

### Added

- `docs/` — doctrine guides: `scheduled-tasks.md` (unattended orchestration: standalone
  pre-prompt, access check then stop, working copy, waves of expert agents, GO/NO-GO audits
  by an agent that did not write, second pass, delivery in a proposal folder, logs, traces,
  handoff), `paradigms.md` (solo-dev, mono-agent-with-safeguards, supervised-expert-team,
  independent-go-nogo-gates), `backlogs-and-traces.md` (claude-friendly item format,
  mandatory-trace block, closure gate), `repo-hygiene.md` (two levers: file template and
  repository settings), `README.md` (index).
- `prompts/` — `scheduled-task.preprompt.md` (stored prompt of an unattended run, with the
  failure each block prevents) and `session-init.xml` (opening message of a working session).
- Repository hygiene files: `CODEOWNERS`, `.github/dependabot.yml` (GitHub Actions, weekly),
  `.github/workflows/gitleaks.yml` (secret scan of every push and pull request, whole history
  weekly and on demand; actions pinned by full SHA),
  `.githooks/pre-commit` (gitleaks on staged changes), `.gitattributes`, `.editorconfig`.
- `ORCHESTRATEUR.md` 2.3.0: `<themes>` with phase conventions, `<paradigms>`,
  `<scheduled-tasks>`, `<token-economy>`; rules `project-table`, `lock-diff`,
  `nothing-deleted`, `git-delegation`; guardrail `auditor-independence`; session mode
  `scheduled`; map of the file in `<purpose>`.
- `AGENT.md` 2.3.0: `<universal-backlog-trace>` rules `brief-trace`, `orchestrator-relay`,
  `closure-gate`; principles `test-agile`, `model-economy`, `agent-budget`; universal rules
  `nothing-deleted`, `project-new` (registration card + diff), `operator-env`.
- `skills/skill-root/SKILL.md` 2.3.0: `team-mode` hook (solo-dev / team, Definition of Done,
  sprint cadence, fan-out note), example router rule `workspace-hygiene`, guard 13.

### Changed

- `AGENT.md` `<git-rules>`: agents never run git or gh in write mode, even after a chat
  approval; they prepare the exact command and the operator runs it. Read-only git is listed
  and stays free; background agents put the command in their trace.
- `ORCHESTRATEUR.md`: active projects grouped by theme, with `theme`, parseable `phase`,
  `paradigm` and `escalation-model-tier`; `backlogs-dual` relaxed (human-friendly optional);
  `agent-logs-format` carries the trace template to paste in every brief.
- `skill-root` guard 12 aligned on the new git rule and on "nothing deleted".
- `SECURITY.md`: private disclosure channel first, repository rules section, advice for
  publishing an instance.
- `README.md`: "What's new in v2.3.0", installation copies `docs/` and `prompts/`, file
  structure with `_proposals/` and `_to-delete/`, key concepts (git, nothing deleted,
  scheduled tasks).
- `LICENSE`: copyright line simplified.
- Smaller alignments: orchestrator log path `YYYY-MM-DD-HHMM-{slug}.md`; operator-env pointer in
  `<operator-context>` and two new `<context-files>` entries; self-execution exception in
  `multi-agents-default`; scheduled-tasks row in the skill's named hooks; trace format
  `model-tier` + `model-id` in every example.
- Internal folder names harmonised in English: `control-center` (log scope),
  `.claude/context/projects/`, `template-folder/`.
- `LLM-ARCHITECTURE.md`: git actions are run by the operator from commands the agents prepared.
- `README.md`: installation copies `docs/`, `prompts/` and `TOKEN-ECONOMY.md` to the workspace
  root and creates the target folders first; dual-backlog section aligned (human-friendly
  optional); example values made neutral.

### Fixed

- `.gitignore`: legacy entries inherited from a private workspace removed; they excluded
  `/.github/`, `/docs/…` files, `/templates/`, `/tests/` and `/examples/`, which would have
  silently kept the new workflow and docs out of the repository.
- `AGENT.md` `<init-bootstrap>`: "4 root files" corrected to 5 (the skill was added in 2.2.0);
  step 6 no longer claims that the CHANGELOG is git-ignored.
- `README.md`: same "4 root doctrine files" correction.

## [2.2.0] — 2026-09-02

### Added

- `skills/skill-root/SKILL.md` — a root orchestrator **skill** that complements the root
  `AGENT.md`: INIT-SESSION hook (skills inventory, MCP inventory, environment detection
  LOCAL / NOMAD, VERSION-CHECK, 5-line announcement), continuous announcement of every skill
  or MCP server mobilised, opt-out and degraded mode, `availability-constraints` hook for any
  schedule proposal, 17 example router rules with combos, MCP doctrine, 12 permanent guards,
  automatic inferences. Fully placeholder-based (`{{OPERATOR_NAME}}`, `{{WORK_DAY_HOURS}}`…).
- `scripts/check-router.py` — anti-drift check: reports workspace skills not routed by
  skill-root, broken "routed by skill-root" back-references, and router targets with no
  directory. Standard library only, CI-friendly exit code.
- `SECURITY.md` — no-secrets policy for the template, disclosure contact, recommended
  `.gitignore` and pre-push scan.
- `CHANGELOG.md` — this file (the README linked to it since 2.0.0 but it was git-ignored).
- New placeholders: `OPERATOR_LOCATION`, `OPERATOR_OS`, `OPERATOR_AUDIENCES`,
  `OPERATOR_COGNITIVE_STYLE`, `OPERATOR_COGNITIVE_STYLE_NOTE`, `OPERATOR_TAX_STATUS`,
  `STUDENT_LEVELS`, `UNROUTED_ALLOWLIST`, `WORK_DAY_HOURS`, `EARLIEST_START`,
  `PREFERRED_DAY_OFF`, `VALID_DAY_PATTERNS`, `CALENDAR_SOURCE`.

### Changed

- `AGENT.md` — version 2.2.0; `<init-bootstrap>` now also scans `skills/skill-root/SKILL.md`
  and knows the new placeholders; `<skills-pointer>` added next to `<mcp-integrations>`.
- `README.md` — "What's new in v2.2.0", "Skill layer" section, placeholder table extended,
  version badge 2.2.0.
- `.gitignore` — `CHANGELOG.md` is no longer ignored; MCP configuration files, `.env*`,
  `.claude/settings.local.json` and `.claude/secrets/` are now excluded.

### Security

- Template files never carry a credential: MCP configurations are referenced by environment
  variable (`${VAR}`) and excluded from version control (see `SECURITY.md`).

## [2.1.0] — 2026-04

### Added

- `TOKEN-ECONOMY.md` with per-task / per-tier projections and the interactive SVG dashboard
  `token-economy-dashboard.html`.

## [2.0.0] — 2026-04-15

### Changed (breaking)

- `CLAUDE.md` renamed to `AGENT.md` for multi-model compatibility.
- Format migrated from markdown to XML hybrid minimalist; LOCK markers replaced by the
  `lock="true"` attribute.
- `<universal-backlog-trace>` introduced as cornerstone; ten session rules moved to
  `ORCHESTRATEUR.md`.
- `<init-bootstrap>` self-cleaning mechanism; full English documentation.
