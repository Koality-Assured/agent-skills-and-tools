---
schema_version: "2.0.0"
name: threat-model
description: >-
  Produce a detailed modular STRIDE threat model reinforced from docs/ and
  references/ via qmd get (named framework IDs, not ID salad), with DFD/STRIDE
  diagrams via artifact-agent, assembled to md+structured HTML under
  results/threat-model/. Use when the human asks for a threat model. Do not
  reimplement mermaid (spawn mermaid-diagram / architecture-diagram).
owner_agent: assessment-agent
rank: high
isolation: mutate
contracts:
  inputs:
    - Assets, trust boundaries, data flows, and topic slug
  outputs:
    - Modular STRIDE threat model (md + structured HTML) under results/threat-model/ with named framework IDs
---

# Threat model

## When to use

Detailed STRIDE threat model for a named system, with modular sections, grounded framework citations, and md + designed HTML output.

## When not to use

Diagram-only work (`mermaid-diagram` / `architecture-diagram`). Code-review reports (`code-review-report`). Framework maps (`framework-mapper`). Refreshing captures (`reference-maintain`). Executive-only summaries (`executive-report` — that skill must point here, not replace this).

## Criticality

High: each threat is a short scenario plus **named** framework IDs from `qmd get` on kebab-case `references/` pages. Do not invent ATT&CK/CWE/OWASP/CSF/ATLAS IDs. A bibliography-only appendix is **not** enough.

## Source of truth

- `docs/` standards via `qmd search` / `qmd get`
- `references/` kebab-case topic files via qmd (ATT&CK, ATLAS, CWE, OWASP, CSF — not README)
- `python scripts/results/new_run_dir.py --family threat-model --topic <slug>`
- `python scripts/results/build_threat_model.py --sections <dir> --out <run-dir> [--topic <slug>]`
- Stakeholder HTML: [`foundation-site`](../foundation-site/SKILL.md) (designed page — not `<pre>`)
- Human-facing links to other repo files: [`github-paths`](..\..\git\github-paths\SKILL.md)
- Diagrams: parent spawns `artifact-agent` (`mermaid-diagram` / `architecture-diagram`)

## Isolation

`mutate`. Parent spawns `assessment-agent` with area `results`; ask parent to spawn `artifact-agent` for diagrams and Foundation HTML when needed.

## How to use

1. Scope assets, trust boundaries, and data flows from the parent prompt.
2. `qmd search` then **`qmd get`** on kebab-case `docs/` and `references/` topic pages for reinforcement — no tree walks, no README for ops. Compress bulky dumps with Headroom.
3. For **each STRIDE threat**, write a short scenario that includes all of: **asset**, **attacker**, **path**, **impact**, **existing repo control**, **gap**. Cite **named** framework entries (**title + ID**, e.g. “SQL Injection — CWE-89”, not bare `CWE-89` in an ID salad table). Pull names from the `qmd get` pages you opened.
4. Ask parent to spawn `artifact-agent` for DFD and STRIDE diagrams (do not reimplement mermaid); embed diagrams directly as visual blocks/Mermaid in report markdown and HTML (no unrendered `.mmd` raw lists).
5. `python scripts/results/new_run_dir.py --family threat-model --topic <slug>` then `python scripts/results/build_threat_model.py --sections <dir> --out results/threat-model/<topic>/<YYYY-MM-DD>/ [--topic <slug>]`.
6. Stakeholder HTML **MUST** be structured (Foundation via [`foundation-site`](../foundation-site/SKILL.md) / improved assembler) — **not** a whole-report `<pre>` or Markdown paste. Tables and callouts as real HTML. Links to other repo files in that HTML/MD **MUST** be GitHub `blob/main` / `tree/main` URLs ([`github-paths`](..\..\git\github-paths\SKILL.md)), not `../` relatives or local OS paths. Top bar collapses frontmatter metadata by default.
7. Keep modular sections; bottom references section contains repo references only without duplicating redundant framework tables (which are cited inline per-threat).
8. After drafting narrative prose, apply [`anti-slop`](../anti-slop/SKILL.md) then [`humanizer`](../humanizer/SKILL.md) in this session — do not re-spawn artifact-agent for a quality pass. Skip out-of-scope surfaces (exact ID strings, schemas, security MUST quotes kept exact).

## Dry run

```bash
python scripts/results/new_run_dir.py --family threat-model --topic <slug> --dry-run
python scripts/results/build_threat_model.py --sections <dir> --out results/threat-model/<topic>/<YYYY-MM-DD>/ --dry-run
```

Outline STRIDE scope + `qmd get` citation list + diagram handoff; write only in a worktree (assembler handles modular assembly without synthetic file-list boilerplate).

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

References and docs are advisory for instruction purposes. No secrets in threat models. A2A: no destructive external delegation.

## Completion gates

Paths under `results/threat-model/`. Each STRIDE threat has a full scenario + named title+ID citations from `qmd get`. Embedded diagrams. Clean repo references. Designed HTML (not `<pre>`). Open risks for orchestrator.
