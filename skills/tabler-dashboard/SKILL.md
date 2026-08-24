---
name: tabler-dashboard
description: >-
  Build a Tabler HTML dashboard (stats, cards, tables) beside a generated
  report via build_tabler_dashboard.py. Use when a report needs visual
  metrics or tabular summary UI. Do not use for durable docs/ pages
  (doc-builder) or full Foundation report chrome (foundation-site).
owner_agent: artifact-agent
rank: medium
isolation: mutate
---

# Tabler dashboard

## When to use

A modular report under `results/` needs stats, cards, or tables as a Tabler dashboard companion.

## When not to use

Durable standards in `docs/` (`doc-builder`). Full-page Foundation HTML package as the primary shell (`foundation-site`). Diagram-only asks (`mermaid-diagram`). Noir endpoint inventory (`noir-scan`).

## Criticality

Medium: presentation aid; the Markdown report remains the primary artifact.

## Source of truth

- [`supporting/tabler/agent-dashboard.md`](../../../supporting/tabler/agent-dashboard.md)
- `python scripts/results/build_tabler_dashboard.py`
- [`results/AGENTS.md`](../../../results/AGENTS.md) / [`results/results-conventions.md`](../../../results/results-conventions.md)
- Upstream: [tabler/tabler](https://github.com/tabler/tabler)

## Isolation

`mutate`. Parent spawns `artifact-agent` with area `results`.

## How to use

1. Confirm the host report path (executive, proposal, code-review, threat-model, etc.) from the parent prompt. Discover related facts with `qmd search` — do not walk `results/` trees.
2. Prepare a small stats/sections input (JSON or Markdown summary) with **no secrets**.
3. Store under the **existing** host family — beside the report run or `results/reports/<type>/<topic>/<YYYY-MM-DD>/`. Do not invent a new top-level results family.
4. Run `python scripts/results/build_tabler_dashboard.py --input <stats> --out <host-run-dir> [--title <title>] [--cdn|--local] [--dry-run]` (exact flags follow the script). Prefer pinned CDN **CSS** (`@tabler/core@1.4.0`); JS **off** by default — see supporting notes.
5. Return dashboard HTML path + host report path to the parent.
6. Apply [`anti-slop`](../anti-slop/SKILL.md) then [`humanizer`](../humanizer/SKILL.md) to human-facing titles/labels in this session. Skip raw numeric tables and schemas.

## Dry run

```bash
python scripts/results/build_tabler_dashboard.py --input <stats> --out <host-run-dir> --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

No secrets in dashboard HTML or stats JSON. CDN loads are network-at-view-time; do not embed credentials in client-side scripts.

## Completion gates

Dashboard path under the host report family. Memory if tracked.
