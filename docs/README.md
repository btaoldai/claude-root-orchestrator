# Doctrine guides

These guides explain the rules that `AGENT.md` and `ORCHESTRATEUR.md` state in one line each.
Read the rule first, then the guide when you need the why and an example.

| Guide | Rule it explains | Read it when |
|---|---|---|
| [scheduled-tasks.md](./scheduled-tasks.md) | ORCHESTRATEUR.md `<scheduled-tasks>` | you want an orchestration to run unattended (nightly sprint, release preparation, audit) |
| [paradigms.md](./paradigms.md) | ORCHESTRATEUR.md `<paradigms>` | you choose how a project is run : who does the work, who closes a step |
| [backlogs-and-traces.md](./backlogs-and-traces.md) | AGENT.md `<universal-backlog-trace>`, ORCHESTRATEUR.md `backlog-event-driven`, `agent-logs-format` | you brief a sub-agent or write a backlog item |
| [repo-hygiene.md](./repo-hygiene.md) | AGENT.md `<git-rules>`, `SECURITY.md` | you create a repository or make one public |

Prompt templates live in [`../prompts/`](../prompts/) :

- [`session-init.xml`](../prompts/session-init.xml) — opening message of an interactive working session ;
- [`scheduled-task.preprompt.md`](../prompts/scheduled-task.preprompt.md) — stored prompt of an unattended run.

## What these guides are not

- Not a tutorial for a given assistant : the rules are written for any assistant that reads instruction files and can spawn sub-agents.
- Not your workspace : every name below (`project-alpha`, `_to-delete/`, paths) is an example to rename.
