# Repository hygiene — two levers

> Related : AGENT.md `<git-rules>`, [`../SECURITY.md`](../SECURITY.md).

## Concept

GitHub separates two things people tend to confuse : the **files** of a repository and the **settings** of a repository. A template repository copies files but never a setting ; a settings script never creates a project file. Treat them as two levers and pull both.

| Lever | What it covers | Tool |
|---|---|---|
| 1. File template | `.gitignore`, `.gitattributes`, `.editorconfig`, `SECURITY.md`, `CODEOWNERS`, `.github/dependabot.yml`, a secret-scanning workflow, a pre-commit hook, skeletons for `README`, `CHANGELOG`, `AGENT.md`, `docs/adr/` | a private template repository of your own (this repository ships an example of each hygiene file ; the skeletons are yours to write) |
| 2. Repository settings | ruleset on the default branch, secret scanning and push protection, Dependabot alerts, Actions permissions, wiki and projects closed, merged branches deleted | a script calling the GitHub API through `gh` (idempotent, re-runnable on an existing repository) |

## What this repository ships for lever 1

| File | Role |
|---|---|
| `.gitignore` | secrets and local configuration never versioned (`.env*`, MCP configs, local assistant settings, keys) ; logs, backlogs and `_to-delete/` stay local |
| `.gitattributes` | LF line endings everywhere, binaries marked |
| `.editorconfig` | UTF-8, LF, final newline, indentation |
| `SECURITY.md` | private disclosure channel, no-secret policy, pre-push checks |
| `CODEOWNERS` | default reviewer of every pull request, Dependabot included |
| `.github/dependabot.yml` | weekly updates of the GitHub Actions used by the workflows |
| `.github/workflows/gitleaks.yml` | secret scan of the commits of every push and pull request, of the whole history weekly and on demand ; actions pinned by full commit SHA, tag in comment |
| `.githooks/pre-commit` | refuses a commit containing a secret (gitleaks) ; enable with `git config core.hooksPath .githooks` |

## Recommended settings (lever 2)

| Setting | Value | Why |
|---|---|---|
| Visibility | private by default | a public repository is prepared (publication guard, licence, clean history) ; it is not "switched" |
| Ruleset on the default branch | no deletion, no force push, linear history | a reference branch that does not get rewritten ; pull requests merged by squash or rebase |
| Secret scanning + push protection | enabled (always available on public repositories) | GitHub blocks a push that contains a recognised token ; the pre-commit hook does the same earlier, offline |
| Account-level push protection | "Push protection for yourself" on | covers every push of the account, private repositories included |
| Dependabot | alerts on ; update pull requests per ecosystem | knowing without being flooded by unreviewed pull requests |
| Actions | allow-list (GitHub-owned + explicit patterns), `GITHUB_TOKEN` read-only, full-SHA pinning required | a third-party action is code executed with your rights ; a tag can be moved, a SHA cannot |
| Wiki, Projects | closed | documentation lives in the repository ; less surface |
| Merged branches | deleted automatically | a readable repository |
| Public repository extras | code scanning, required status checks once CI is green, `LICENSE` | what a reader and a contributor expect |

Some settings are refused by the API depending on the plan (for example secret scanning on a private repository of a free plan, or SHA-pinning enforcement) : a good script reports them and continues ; set them by hand in Settings.

## Before every first push : three questions

```bash
git rev-parse --show-toplevel        # where am I ?
git status --short                   # what leaves ?
git diff --cached --name-only
git remote -v                        # where to ?
```

## What it does not do

- It does not push code, delete anything or rewrite history : those actions stay with the operator.
- It does not make a private repository publishable : decision records and logs can name third parties or predecessors ; publication goes through a dedicated guard and, if needed, a new repository with a clean history.
- It does not replace reading the README and CHANGELOG before a push : a wrong sentence on the front page is the first thing a reader sees.
