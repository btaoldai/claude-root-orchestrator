---
tags:
  - claude/instructions
  - llm-architecture
  - multi-model
version: 2.0.0
created: 2026-03-31
updated: 2026-04-14
author: "{{OPERATOR_NAME}}"
changelog: |
  v2.0.0 - XML hybrid conversion, renamed from Claude-specific to multi-model template (AGENT.md compatible), full English
  v1.0.0 - initial markdown version with ASCII diagram
---

# LLM Architecture — Multi-Model Collaboration

> Version 2.0.0 | Last updated : {{DATE}}

<llm-architecture version="2.0.0">

<overview>
This document describes the collaboration architecture between multiple LLMs used in parallel for complex software development and project management with AI coding assistants (Claude Code, Cursor, Aider, and compatible tools). The model selection pattern maps tasks to the LLM best suited for them, maintaining human-in-the-loop validation at each stage.
</overview>

<general-architecture>
```
                          +---------------------+
                          |     OPERATOR        |
                          |  {{OPERATOR_NAME}}  |
                          |  (human in loop)    |
                          +----------+----------+
                                     |
              +---------------------+---------------------+
              |                     |                     |
   +----------v---------+  +--------v--------+  +--------v--------+
   |   HIGH-TIER LLM    |  |   MID-TIER LLM  |  |  LOW-TIER LLM  |
   |                    |  |                  |  |                 |
   | - Critical code    |  | - Documentation  |  | - Quick search  |
   | - Security audit   |  | - Refactoring    |  | - Navigation    |
   | - Architecture     |  | - Courses/slides |  | - Simple Q&A    |
   | - Complex debug    |  | - Organization   |  | - Read-only     |
   +--------------------+  +------------------+  +-----------------+
                                     |
                          +----------v----------+
                          | EXTERNAL RESEARCH   |
                          | (Perplexity/Gemini) |
                          |                     |
                          | - Tech watch        |
                          | - Web research      |
                          | - Up-to-date docs   |
                          | - CVE / advisories  |
                          +---------------------+
```

The template is model-agnostic. Map your preferred LLMs to the three tiers below. Common mappings :

| Tier | Anthropic | OpenAI | Google | Meta | Mistral |
|------|-----------|--------|--------|------|---------|
| high | Claude Opus | GPT-4 Turbo, GPT-4o | Gemini 1.5 Pro | Llama 3.1 405B | Mistral Large |
| mid | Claude Sonnet | GPT-4o mini | Gemini 1.5 Flash | Llama 3.1 70B | Mistral Medium |
| low | Claude Haiku | GPT-3.5 Turbo | Gemini Nano | Llama 3.1 8B | Mistral Small |
</general-architecture>

<models-and-responsibilities>

<model-tier id="high" role="architect-auditor">
<examples>Claude Opus, GPT-4 Turbo, GPT-4o, Gemini 1.5 Pro, Llama 3.1 405B, Mistral Large, DeepSeek-V3.</examples>
<use-case>Production code, security audit, architecture decisions.</use-case>
<when-to-use>Critical tasks : auth, crypto, production infra, complex components.</when-to-use>
<when-not-to-use>Quick lookups, navigation, simple tasks (token overhead).</when-not-to-use>
<permissions>Read/write on all non-LOCK files.</permissions>
<lock-rights>Only tier allowed to propose LOCK modifications (with operator approval).</lock-rights>
<paradigm>Zero-Trust, Secure-by-Design, systematic audit.</paradigm>
</model-tier>

<model-tier id="mid" role="writer-refactorer">
<examples>Claude Sonnet, GPT-4o mini, Gemini 1.5 Flash, Llama 3.1 70B, Mistral Medium, DeepSeek-Coder.</examples>
<use-case>Documentation, refactoring, pedagogical materials, slides.</use-case>
<when-to-use>Medium-criticity tasks, non-LOCK files, writing work.</when-to-use>
<when-not-to-use>Critical code, auth/crypto systems, security audit.</when-not-to-use>
<permissions>Read/write on non-LOCK files.</permissions>
<lock-rights>Read only on LOCK files.</lock-rights>
<paradigm>Clarity, structure, style consistency.</paradigm>
</model-tier>

<model-tier id="low" role="reader-navigator">
<examples>Claude Haiku, GPT-3.5 Turbo, Gemini Nano, Llama 3.1 8B, Mistral Small, Phi-3.</examples>
<use-case>Quick lookups, vault navigation, simple questions.</use-case>
<when-to-use>DISCUSSION mode, simple agent delegation, read-only operations.</when-to-use>
<when-not-to-use>Any writing task, audit, architecture.</when-not-to-use>
<permissions>Read only (strictly).</permissions>
<lock-rights>Read only.</lock-rights>
<paradigm>Token savings, speed, precision.</paradigm>
</model-tier>

<model-tier id="external-research" role="live-web-knowledge">
<examples>Perplexity, Gemini (web mode), ChatGPT Search, You.com.</examples>
<use-case>Tech watch, up-to-date documentation lookup, CVE.</use-case>
<when-to-use>Before coding a feature (verify existing solutions), precedent research.</when-to-use>
<when-not-to-use>Production code, architectural decisions (no traceability).</when-not-to-use>
<permissions>No workspace permission.</permissions>
<integration>Results synthesized by the orchestrator before integration into any artifact.</integration>
<paradigm>Internet access, recent information, multiple sources.</paradigm>
</model-tier>

</models-and-responsibilities>

<development-workflow>
<description>Typical development cycle with the multi-LLM system.</description>
<phase n="1" name="research">
<agent>Perplexity / Gemini</agent>
<action>Research : libraries, CVEs, best practices, official documentation.</action>
<output>Markdown synthesis in `.claude/context/research-YYYYMMDD.md`.</output>
</phase>
<phase n="2" name="architecture">
<agent>High-tier model (Winston persona)</agent>
<action>System design based on the research.</action>
<output>ADR plus C4 diagrams plus RBAC.</output>
</phase>
<phase n="3" name="implementation">
<agent>High-tier model (Amelia or Winston persona)</agent>
<action>Production code, unit tests, integration.</action>
<validation>Tests + lint + audit (adapt to your stack).</validation>
</phase>
<phase n="4" name="documentation">
<agent>Mid-tier model (Paige persona)</agent>
<action>README, inline docs, changelog, pedagogical supports.</action>
</phase>
<phase n="5" name="security-review">
<agent>High-tier model (Quinn or Sam persona)</agent>
<action>Audit produced code, threat model, RBAC validation.</action>
<output>Audit report with risk score.</output>
</phase>
<phase n="6" name="operator-validation">
<agent>{{OPERATOR_NAME}} (human)</agent>
<action>Review deliverables, validate LOCK decisions.</action>
<trigger>Git actions (commit, push, merge).</trigger>
</phase>
</development-workflow>

<inter-llm-collaboration-rules>
<context-isolation>
Each LLM receives only the minimal context needed for its task (least privilege).
Results from Perplexity/Gemini are always synthesized by Claude before integration.
No external output is committed raw into the repo.
</context-isolation>
<handoff>
When an agent finishes and hands over :
1. It produces an explicit deliverable (file or report).
2. It logs its work in `.claude/logs/agents/`.
3. The orchestrator validates the deliverable before the next phase.
4. The orchestrator log records the transition.
</handoff>
<file-conflicts>
Two agents cannot write to the same file in parallel.
The orchestrator reserves files before delegation.
On conflict : the higher-tier agent (high > mid > low) has priority.
</file-conflicts>
<secrets-credentials>
No LLM receives credentials, tokens, or secrets in plaintext.
`.env` files and secrets are excluded via `.claudeignore`.
Security audits work on code, never on secrets.
</secrets-credentials>
</inter-llm-collaboration-rules>

<ai-fluency-principles>
<reference>Applied methodology : Anthropic AI Fluency Framework — Foundations (https://anthropic.skilljar.com/ai-fluency-framework-foundations).</reference>

<principle id="practical">
Every LLM interaction produces a concrete artifact :
Code = source file + tests.
Architecture = diagram + ADR.
Documentation = structured markdown file.
Research = synthesis in `.claude/context/`.
</principle>

<principle id="efficient">
Optimal-model routing avoids overhead :
High-tier is not used for simple vault navigation.
Low-tier does not produce critical code.
Perplexity/Gemini does not replace architectural decision (it informs it).
</principle>

<principle id="ethical">
Full transparency on LLM usage :
Every session is logged (who did what, with which model).
Commits mention the LLM collaboration.
No hidden automation : the operator always validates important actions.
</principle>

<principle id="safe">
Zero-Trust by default on LLM outputs :
Any produced code is reviewed before integration.
LOCK files cannot be modified without explicit human approval.
Git actions are always operator-triggered, never autonomous.
Credentials never transit through an LLM.
</principle>
</ai-fluency-principles>

<tracking-metrics optional="yes">
For workspaces with heavy usage, monitor :

| Metric | Target | Tool |
|--------|--------|------|
| Agent delegation success rate | above 90% | Orchestrator logs |
| High/mid/low-tier ratio | Balanced per load | Session logs |
| LOCK files modified without approval | 0 | Git audit |
| Open anomalies older than 7 days | 0 | ORCHESTRATEUR.md history |
| Synchronized backlogs | 100% | .claude/backlogs/ |
</tracking-metrics>

<references>
AI Fluency Framework : https://anthropic.skilljar.com/ai-fluency-framework-foundations
Claude Code Documentation : https://docs.anthropic.com/claude/docs/claude-code
Anthropic Model Overview : https://docs.anthropic.com/claude/docs/models-overview
AGENT.md ROOT : `AGENT.md` (workspace root)
Agent routing : `00-control-center/ORCHESTRATEUR.md`
</references>

</llm-architecture>
