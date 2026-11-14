# Paradigms — how a project is run

> Rule : ORCHESTRATEUR.md `<paradigms>`. Each project declares its paradigm(s) in the `paradigm` attribute of its entry ; several can be combined (for example `paradigm="supervised-expert-team independent-go-nogo-gates"`).

## Concept

A paradigm answers two questions the routing table alone does not : **who does the work** and **who decides that a step is closed**. Writing it down per project keeps the orchestrator from improvising a different organisation at every session.

## The paradigms

### solo-dev

- **What it is** : one human, the operator. Personas (architect, developer, QA, security, scribe) are hats worn by the orchestrator, not distinct people.
- **What it does** : AI sub-agents are allowed for parallel production or verification ; validation stays 100 % with the operator ; the Definition of Done of the skill layer applies to every increment.
- **What it does not do** : no cross-review between humans, no shared sprint planning ; it does not justify spawning agents for a task one writer and one reviewer can do.

### mono-agent-with-safeguards

- **What it is** : one agent at a time, with domain quality gates (spelling, accuracy of references, no ready-made answers in teaching material...).
- **What it does** : runs the gates before delivery and refuses to deliver when one fails.
- **What it does not do** : no parallel waves ; fit for content where consistency matters more than speed.

### supervised-expert-team

- **What it is** : the organisation of the work. A team of expert agents (developer, auditor, fact-checker, analyst, librarian...) launched in waves and supervised by the orchestrator.
- **What it does** :
  - splits the work into parallel waves, each agent with a role, a tool budget and a mandatory trace ;
  - re-reads and re-checks every delivery (re-runs the tests and checks itself) before writing anything to the workspace ;
  - consolidates, corrects, relaunches or asks the operator until the result holds ;
  - combines naturally with *independent-go-nogo-gates*, which says when a step is closed.
- **What it does not do** : it does not decide for the operator (decisions are presented with the reasons for, against, and a recommendation) ; no agent publishes or runs git in write mode.

### independent-go-nogo-gates

- **What it is** : gatekeeping. The project moves gate by gate (G0 framing ... G8 delivery), without a calendar.
- **What it does** :
  - a pre-mortem at the opening of each gate ("imagine it failed : why ?") produces measurable exit criteria ;
  - the gate closes on the verdict GO, GO WITH CONDITIONS or NO-GO of an expert who **did not produce** the work ;
  - counter-audit until GO ; the next gate opens as soon as the previous one is green.
- **What it does not do** : it does not set dates ; it never accepts an auditor who produced what he audits.

## Choosing

| Situation | Paradigm |
|---|---|
| Small tool, one evening of work | solo-dev |
| Course material, documentation with strict quality rules | mono-agent-with-safeguards |
| Large sprint with code, content and audits in parallel | supervised-expert-team |
| Infrastructure, security, anything costly to roll back | independent-go-nogo-gates (often with supervised-expert-team) |
