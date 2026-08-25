---
schema_version: "2.0.0"
name: product-opportunity-scout
description: >-
  Scouts emerging developer products, software opportunities, unmet developer pain points,
  and tooling gaps by analyzing developer discussions, product launches, and forum complaints.
  Use when exploring new product ideas, assessing market white-spaces in developer tooling/AI,
  or identifying tooling gaps in existing ecosystems. Do not use for commercial pricing
  comparisons alone (benchlm-lookup).
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
      sector:
        type: string
        description: Ecosystem sector (e.g. MCP tooling, context caching, local inference, code review)
      lens:
        type: string
        description: Opportunity focus (e.g. pain points, tooling gap, indie product alternatives)
  outputs:
    task_id: string
    status: string
    artifacts: list
    handoff_requests: list
    metrics: dict
---

# Product opportunity scout

## When to use

Identifying emerging developer products, commercial white-spaces, recurring unmet tooling needs, developer friction points, and indie product opportunities by analyzing discussions on Hacker News (`Show HN`, `Ask HN`), Reddit (`r/LocalLLaMA`, `r/devops`), Product Hunt, and GitHub Discussions.

## When not to use

Pure model token price lookups (use `benchlm-lookup`). Vendor API changelog monitoring (use `ai-vendor-updates`). Formal architecture proposal authoring (use `proposal-report`).

## Criticality

High: Grounding product and tooling initiatives in verified, recurring developer pain points prevents building unused features and highlights high-leverage tooling opportunities.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/community_analyzer.py`](../../../../scripts/research/community_analyzer.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Opportunity dossiers write under `results/research/community/product-opportunities/<sector>/<YYYY-MM-DD>/`.

## How to use

1. Scan high-signal developer communities for recurring friction points:
   ```bash
   python scripts/research/community_analyzer.py --topic devops --min-tier Tier 1
   ```
2. Cluster user complaints into distinct problem statements:
   - **Problem Intensity**: How acute is the friction? Is it blocking production workflows?
   - **Existing Workaround Quality**: Are existing solutions complex, expensive, or brittle?
   - **Market Gap**: What tooling primitive is missing (CLI, proxy, MCP server, visualizer)?
3. Outline proposed tooling concepts, target user personas, and differentiation angles.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill product-opportunity-scout --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Do not endorse speculative hype without validating developer demand against real complaints and discussions.

## Completion gates

Confirm structured product opportunity dossier is written under `results/research/community/product-opportunities/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
