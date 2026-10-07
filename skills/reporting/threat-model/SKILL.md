---
schema_version: "2.0.0"
name: threat-model
description: >-
  Produce a detailed modular STRIDE threat model reinforced from docs/ and
  references/ via qmd get (named framework IDs), with DFD/STRIDE diagrams
  through the destination's local diagram workflow, assembled to Markdown and
  structured HTML under the destination's output convention. Use when the
  human asks for a threat model. In ai-router, `artifact-agent` routes diagram
  work to `mermaid-diagram` / `architecture-diagram`; standalone repositories
  use local diagram tools or create Mermaid in-session when permitted, and
  report a capability gap when no supported path exists.
owner_agent: security-tooling-operator
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
- Human-facing links to other repo files: [`github-paths`](../../git/github-paths/SKILL.md)
- Diagrams: in ai-router, the parent may hand off to `artifact-agent` (`mermaid-diagram` / `architecture-diagram`). Standalone repositories use local dispatch or create the diagram in-session where permitted; report a capability gap if no supported path exists.

## Isolation

Standalone dispatch: Follow the destination's isolation and dispatch rules. Use a registered local operator or continue in-session when those rules permit; report a capability gap if no local path supports the work.

`mutate`. In ai-router, the parent spawns `assessment-agent` with area `results` and may hand diagram or Foundation HTML work to `artifact-agent`. Standalone repositories follow local dispatch and output rules, continue in-session where permitted, or report a capability gap.

## How to use

1. Scope assets, trust boundaries, and data flows from the parent prompt.
2. `qmd search` then **`qmd get`** on kebab-case `docs/` and `references/` topic pages for reinforcement — no tree walks, no README for ops. Compress bulky dumps with Headroom.
3. For **each STRIDE threat**, write a short scenario that includes all of: **asset**, **attacker**, **path**, **impact**, **existing repo control**, **gap**. Cite **named** framework entries (**title + ID**, e.g. “SQL Injection — CWE-89”, not bare `CWE-89` in an ID salad table). Pull names from the `qmd get` pages you opened.
4. In ai-router, ask the parent to hand DFD and STRIDE diagrams to `artifact-agent`. Standalone repositories follow local dispatch rules or create the diagram in-session when permitted; report a capability gap when no supported path exists. Embed diagrams directly as visual blocks/Mermaid in report markdown and HTML.
5. `python scripts/results/new_run_dir.py --family threat-model --topic <slug>` then `python scripts/results/build_threat_model.py --sections <dir> --out results/threat-model/<topic>/<YYYY-MM-DD>/ [--topic <slug>]`.
6. Stakeholder HTML **MUST** be structured (Foundation via [`foundation-site`](../foundation-site/SKILL.md) / improved assembler) — **not** a whole-report `<pre>` or Markdown paste. Tables and callouts as real HTML. Links to other repo files in that HTML/MD **MUST** be GitHub `blob/main` / `tree/main` URLs ([`github-paths`](../../git/github-paths/SKILL.md)), not `../` relatives or local OS paths. Top bar collapses frontmatter metadata by default.
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
