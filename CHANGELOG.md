# Changelog

All notable changes to the claude-root-orchestrator template are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
