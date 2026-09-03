# Security policy

## Scope

This repository is a **documentation template** (instruction files for AI coding assistants).
It ships no runtime code except `scripts/check-router.py` (standard library, read-only, no
network). The security surface is therefore about **what people put into the template**
once instantiated, not about the template itself.

## No secrets, ever

- No API key, token, password, bearer, private key or connection string in any versioned
  file, in any prompt, or in any example. MCP server configurations reference secrets by
  environment variable only, e.g. `"OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}"`.
- The following are excluded by `.gitignore` in this template and should stay excluded in
  your instantiated workspace: `.env*`, `.mcp.json`, `.claude/mcp.json`,
  `.claude/settings.local.json`, `.claude/secrets/`, `.claude/logs/`, `.claude/backlogs/`.
- The `skill-root` skill instructs the assistant to **never copy** a key, token or
  environment variable into an answer or a log (INIT-SESSION, step MCP-INVENTORY, guard 12).

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
python3 scripts/check-router.py --root skills/skill-root/SKILL.md --skills-dir .claude/skills
```

## Reporting a vulnerability

Open a private security advisory on GitHub (*Security → Report a vulnerability*) rather
than a public issue. Expect an acknowledgement within a week.
