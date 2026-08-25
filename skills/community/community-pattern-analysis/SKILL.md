---
schema_version: "2.0.0"
name: community-pattern-analysis
description: >-
  Extracts recurring architectural patterns, complaint clusters, adoption trends, and
  consensus shifts across multi-platform developer discussions. Use when analyzing how the
  community is solving recurring engineering problems, identifying emergent architectural
  best practices, or mapping trend velocity across subreddits and forums. Do not use for
  single-issue bug troubleshooting (community-troubleshooting).
owner_agent: community-analyst
rank: high
isolation: mutate
on_failure: continue_with_partial
prerequisites:
  - python
dependencies:
  required_skills:
    - isolate-work
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    type: object
    properties:
      topic:
        type: string
        description: Architectural topic or pattern domain (e.g. multi-agent orchestration, context caching, MCP architecture)
      time_horizon:
        type: string
        description: Historical lookback (e.g. 30d, 90d, 1y)
  outputs:
    task_id: string
    status: string
    artifacts: list
    handoff_requests: list
    metrics: dict
---

# Community pattern analysis

## When to use

Synthesizing multi-source developer discussions to uncover emerging architectural patterns (e.g. MCP tool design, local LLM quantization pipelines, agentic orchestration patterns, hybrid context caching), recurring complaint clusters, and consensus shifts across Reddit, Hacker News, and GitHub Discussions.

## When not to use

Single-issue troubleshooting or error lookup (use `community-troubleshooting`). Vendor flash updates (use `ai-vendor-updates`). Formal architecture diagramming (use `architecture-diagram`).

## Criticality

High: Engineering paradigms frequently evolve in developer discussions before formal codification in textbooks or vendor documentation. Recognizing early patterns guides scalable architectural decisions.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/community_analyzer.py`](../../../../scripts/research/community_analyzer.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Pattern reports write under `results/research/community/patterns/<topic>/<YYYY-MM-DD>/`.

## How to use

1. Select multi-platform discussion communities covering the target topic:
   ```bash
   python scripts/research/community_analyzer.py --topic ai --min-tier Tier 1
   ```
2. Aggregate discussion threads across platforms, identifying:
   - **Pattern Convergence**: Which architectural solutions are independently adopted by multiple teams?
   - **Anti-Patterns & Pitfalls**: What approaches are widely attempted and subsequently abandoned?
   - **Trend Velocity**: Is adoption accelerating, plateauing, or declining?
3. Document pattern taxonomy, trade-offs, and empirical code examples under `results/research/community/patterns/`.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill community-pattern-analysis --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Do not mistake viral social trends for validated security patterns without empirical testing.

## Completion gates

Confirm structured pattern analysis report is written under `results/research/community/patterns/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
