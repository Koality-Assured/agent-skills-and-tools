---
name: foundation-site
description: >-
  Build a designed Foundation Sites HTML report package (tables, callouts,
  XY grid, header/hero) via build_foundation_site.py. Use when executive,
  proposal, code-review, or threat-model output should ship as responsive
  HTML — not a Markdown paste. Do not use for durable docs/ corpus pages
  (doc-builder) or Tabler stats dashboards alone (tabler-dashboard).
owner_agent: artifact-agent
rank: medium
isolation: mutate
---

# Foundation site

## When to use

A generated report (executive, proposal, code-review, threat-model) should ship as a **designed** Foundation for Sites HTML package for stakeholder viewing.

## When not to use

Durable kebab-case pages under `docs/` (`doc-builder`). Stats/cards-only visualization (`tabler-dashboard`). Diagram-only work (`mermaid-diagram`).

## Criticality

Medium: presentation package must be real HTML structure; Markdown/report sections remain the editable source.

## Source of truth

- [`supporting/foundation/agent-site-package.md`](../../../../supporting/foundation/agent-site-package.md)
- `python scripts/results/build_foundation_site.py`
- Artifact links to other repo files: [`github-paths`](..\..\git\github-paths\SKILL.md) / [`supporting/github/github-paths.md`](../../../../supporting/github/github-paths.md)
- [`results/AGENTS.md`](../../../../results/AGENTS.md)
- Upstream: [XY Grid](https://get.foundation/sites/docs/xy-grid.html), [Table](https://get.foundation/sites/docs/table.html), [Callout](https://get.foundation/sites/docs/callout.html)

## Isolation

`mutate`. Parent spawns `artifact-agent` with area `results`.

## How to use

1. Confirm the host report path from the parent (assembled md preferred). Discover context with `qmd search` when needed — no tree walks.
2. Store the package **beside** the host report run under the existing family. Do not invent a new top-level family.
3. Run `python scripts/results/build_foundation_site.py --input <report.md|html> --out <host-run-dir> [--title <title>] [--cdn|--local] [--dry-run]` (prefer CDN; CSS-first — no jQuery unless a plugin is required).
4. The bound script **MUST** produce **designed HTML**, not a Markdown paste in a well/`<pre>`: strip frontmatter; GFM tables → `<table>`; blockquotes → `.callout`; header/hero + XY grid + sectioned `<article>`; print CSS. Never leave pipe-tables or YAML keys (`doc_kind`, etc.) in the page.
5. **Success check:** open `index.html` and confirm `<table>`, `.callout`, and **no** leaked `doc_kind` (or other frontmatter keys).
6. Links in the HTML/MD to **other repo files** (threat model, diagrams, standards) **MUST** be GitHub `blob/main` / `tree/main` URLs via [`github-paths`](..\..\git\github-paths\SKILL.md) — not `../` relatives or local OS paths.
7. Return the HTML entry path (`index.html`) to the parent.
8. Apply [`anti-slop`](../anti-slop/SKILL.md) then [`humanizer`](../humanizer/SKILL.md) to any agent-authored chrome copy in this session. Skip verbatim report body already quality-passed.

## Dry run

```bash
python scripts/results/build_foundation_site.py --input <report> --out <host-run-dir> --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

No secrets in HTML. Do not promote Foundation packages into `docs/` as durable SoT.

## Completion gates

`index.html` under the host report family passes the success check (tables, callouts, no leaked frontmatter). Memory if tracked.
