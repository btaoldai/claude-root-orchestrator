#!/usr/bin/env python3
"""check-router.py — anti-drift check between the skill inventory and the skill-root router.

Why this exists
---------------
A root orchestrator skill (skills/skill-root/SKILL.md) routes requests to specialised
skills through ``<rule id="...">`` blocks. Over time, skills get added to the workspace
without a matching rule, and skills declare "routed by skill-root" without a rule that
actually exists. Both silently degrade the orchestrator. This script makes the drift
visible in one command, without an LLM.

What it checks
--------------
1. Every skill directory (``<skills-dir>/*/SKILL.md``) whose ``name`` is neither loaded by a
   router rule (``<load>`` text) nor listed in the allow-list is reported as UNROUTED.
2. Every skill whose body says "routed by skill-root" (or the French "route par skill-root")
   but has no rule loading it is reported as BROKEN-BACKREF.
3. Every ``<load>`` target that matches no skill directory is reported as MISSING-SKILL
   (informational: the target may live in the assistant, not in the workspace).

Usage
-----
    python3 scripts/check-router.py --root skills/skill-root/SKILL.md --skills-dir .claude/skills
    python3 scripts/check-router.py --allow morning,import-memory

Exit code: 0 when no UNROUTED and no BROKEN-BACKREF finding, 1 otherwise (CI-friendly).
No network, no dependency beyond the standard library, no file is modified.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RULE_RE = re.compile(r'<rule\s+id="([^"]+)"[^>]*>(.*?)</rule>', re.DOTALL)
LOAD_RE = re.compile(r"<(?:load|charger)>(.*?)</(?:load|charger)>", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)
BACKREF_RE = re.compile(r"rout(?:ed|e|é) (?:by|par) \[?\[?skill-root", re.IGNORECASE)
LEAD_TOKEN_RE = re.compile(r"^\s*([a-z0-9][a-z0-9-]*[a-z0-9])")


def router_targets(root_skill: Path) -> dict[str, set[str]]:
    """Return {rule_id: {skill names loaded}} parsed from the root SKILL.md.

    A ``<load>`` value is a list separated by ``+`` or ``|``; only the leading kebab-case
    token of each item is a skill name, the rest is annotation ("(workspace)", "depending
    on the format"). That keeps prose out of the target set.
    """
    text = root_skill.read_text(encoding="utf-8")
    targets: dict[str, set[str]] = {}
    for rule_id, body in RULE_RE.findall(text):
        loaded: set[str] = set()
        for load in LOAD_RE.findall(body):
            for item in re.split(r"[+|]", load.lower()):
                match = LEAD_TOKEN_RE.match(item)
                if match:
                    loaded.add(match.group(1))
        targets[rule_id] = loaded
    return targets


def workspace_skills(skills_dir: Path) -> dict[str, Path]:
    """Return {skill name: SKILL.md path} for every skill directory found."""
    found: dict[str, Path] = {}
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        match = NAME_RE.search(skill_md.read_text(encoding="utf-8", errors="replace"))
        name = match.group(1) if match else skill_md.parent.name
        found[name] = skill_md
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="skills/skill-root/SKILL.md", help="path to the root orchestrator SKILL.md")
    parser.add_argument("--skills-dir", default=".claude/skills", help="directory holding one sub-directory per skill")
    parser.add_argument("--allow", default="", help="comma-separated skill names that are intentionally unrouted")
    parser.add_argument("--no-missing", action="store_true", help="hide MISSING-SKILL lines (targets living in the assistant, not in the workspace)")
    args = parser.parse_args()

    root = Path(args.root)
    skills_dir = Path(args.skills_dir)
    if not root.is_file():
        print(f"error: root skill not found: {root}", file=sys.stderr)
        return 2
    if not skills_dir.is_dir():
        print(f"error: skills directory not found: {skills_dir}", file=sys.stderr)
        return 2

    allow = {a.strip() for a in args.allow.split(",") if a.strip()} | {"skill-root"}
    targets = router_targets(root)
    all_targets = set().union(*targets.values()) if targets else set()
    skills = workspace_skills(skills_dir)

    findings = 0
    for name, path in skills.items():
        if name in allow:
            continue
        routed = name in all_targets
        if not routed:
            print(f"UNROUTED       {name:32s} {path}")
            findings += 1
        if not routed and BACKREF_RE.search(path.read_text(encoding="utf-8", errors="replace")):
            print(f"BROKEN-BACKREF {name:32s} says it is routed by skill-root, no rule loads it")
            findings += 1

    for target in sorted(all_targets - set(skills)) if not args.no_missing else []:
        print(f"MISSING-SKILL  {target:32s} loaded by a rule, no directory in {skills_dir} (may live in the assistant)")

    print(f"\nrules: {len(targets)} · workspace skills: {len(skills)} · findings: {findings}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
