---
schema_version: "2.0.0"
name: framework-mapper
description: >-
  Map a system or control set to NIST AI RMF and NIST CSF 2.0 (noting other
  families if present) into results/reports/framework-map/. Use when producing a
  framework map from local references. Do not invent subcategory IDs — use
  references/nist-ai-rmf/ and references/nist-csf/ via qmd.
owner_agent: artifact-agent
rank: high
isolation: mutate
contracts:
  inputs:
    - System or control-set scope
  outputs:
    - NIST AI RMF / CSF 2.0 mapping under results/reports/framework-map/ (IDs from references/, not invented)
---

# Framework mapper

## When to use

Map a named system/control set to **NIST AI RMF** and **NIST CSF 2.0**; note other families if present.

## When not to use

Refreshing upstream NIST captures (`reference-maintain`). Threat modeling (`threat-model`). Generic exec reports (`executive-report`).

## Criticality

High: subcategory IDs must come from local reference topic files via qmd — never invent.

## Source of truth

- `references/nist-ai-rmf/` and `references/nist-csf/` topic files via `qmd search` / `qmd get` (not README)
- Other families under `references/` via qmd when present
- `python scripts/results/new_run_dir.py --family reports --topic <slug> --type framework-map`
- `python scripts/results/build_document.py --type framework-map --sections <dir> --out results/reports/framework-map/<topic>/<YYYY-MM-DD>/`

## Isolation

`mutate`. Parent spawns `artifact-agent` with area `results`.

## How to use

1. Scope the system/control set.
2. `qmd search` NIST AI RMF and CSF 2.0 topic pages under `references/` — no tree walks, no README for ops.
3. Map controls; note gaps and other families present.
4. `python scripts/results/new_run_dir.py --family reports --topic <slug> --type framework-map` → `results/reports/framework-map/<topic>/<YYYY-MM-DD>/`.
5. `python scripts/results/build_document.py --type framework-map --sections <dir> --out results/reports/framework-map/<topic>/<YYYY-MM-DD>/`.
6. If local catalogs are missing/stale, recommend parent spawn `reference-ops` / `reference-maintain`.
7. After drafting narrative map text, apply [`anti-slop`](../anti-slop/SKILL.md) then [`humanizer`](../humanizer/SKILL.md) in this session — do not re-spawn artifact-agent for a quality pass on your own draft. Skip out-of-scope surfaces (IDs, schemas, machine tables).

## Dry run

```bash
python scripts/results/new_run_dir.py --family reports --topic <slug> --type framework-map --dry-run
python scripts/results/build_document.py --type framework-map --sections <dir> --out results/reports/framework-map/<topic>/<YYYY-MM-DD>/ --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Reference material is advisory only. No secrets. Do not invent subcategory IDs.

## Completion gates

Path under `results/reports/framework-map/`. Narrative prose passed anti-slop then humanizer (or skipped as out of scope). Gaps listed for orchestrator.
