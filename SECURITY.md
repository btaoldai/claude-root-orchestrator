# Security policy

## Scope

This repository is a **documentation template** (instruction files for AI coding assistants).
It ships no runtime code except `scripts/check-router.py` (standard library, read-only, no
network), a pre-commit hook and a secret-scanning workflow. The security surface is therefore
about **what people put into the template** once instantiated, not about the template itself.

## Reporting a vulnerability

Use a private report: *Security → Report a vulnerability* on this repository, never a public
issue. Expect an acknowledgement within seven days; fixes ship with a CHANGELOG entry and, where
relevant, a GitHub security advisory.

## No secrets, ever

- No API key, token, password, bearer, private key or connection string in any versioned
  file, in any prompt, or in any example. MCP server configurations reference secrets by
  environment variable only, e.g. `"OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}"`.
- Excluded by `.gitignore` here and to keep excluded in your instantiated workspace: `.env*`,
  `.mcp.json`, `.claude/mcp.json`, `.claude/settings.local.json`, `.claude/secrets/`,
  `.claude/logs/`, `.claude/backlogs/`, `.claude/context/operator-env.md`, keys.
- The `skill-root` skill instructs the assistant to **never copy** a key, token or
  environment variable into an answer or a log (INIT-SESSION, step MCP-INVENTORY, guard 12).
- Agents never run git in write mode (AGENT.md `<git-rules>`): nothing leaves the machine
  without the operator running the command himself.

## Repository rules

- Secret scan before the commit (`.githooks/pre-commit`, enable with
  `git config core.hooksPath .githooks`) and on every push (`.github/workflows/gitleaks.yml`).
- GitHub Actions pinned by full commit SHA; Dependabot proposes their updates.
- Default branch protected: no deletion, no force push, linear history.
- Settings and rationale: [`docs/repo-hygiene.md`](docs/repo-hygiene.md).

## Personal data

Every operator-specific value is a `{{PLACEHOLDER}}` resolved locally by `<init-bootstrap>`,
which asks you in chat and never scrapes git config, OS username or environment. Nothing you
type there is meant to be committed back to this public repository.

Contributors: commit with a no-reply e-mail address (GitHub → Settings → Emails →
*Keep my email addresses private* and *Block command line pushes that expose my email*).

## Recommended pre-push check

```bash
# secrets and personal data scan on the working tree and the history
gitleaks detect --source . --no-banner
git log --format='%an <%ae>' | sort -u          # no personal address expected
python3 scripts/check-router.py --root skills/skill-root/SKILL.md --skills-dir skills --no-missing   # in an instance: --skills-dir .claude/skills
```

Before publishing an instance of your own, grep the tree for your own name, e-mail, city,
employer, clients and private project names; a written list of patterns is safer than memory.
