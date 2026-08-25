---
schema_version: "2.0.0"
name: social-osint
description: >-
  Conducts structured open-source intelligence (OSINT) gathering across public social platforms,
  developer profiles, commit breadcrumbs, and conference materials. Use when reconstructing
  technical timelines, tracing unannounced feature infrastructure, evaluating researcher
  departure/arrival signals, or mapping public open-source affiliations. Do not use for
  illicit surveillance, private data gathering, or PII harvesting.
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
    - Public organization, project, or initiative and investigation lens
  outputs:
    - Public-signal timeline or affiliation map with sources; no private-data or PII collection
---

# Social OSINT

## When to use

Gathering public technical intelligence from open-source repositories, public issue tracker discussions, researcher presentations, public social posts, and package release histories. Use to uncover technical breadcrumbs, unannounced model architecture changes, deprecation timelines, or organizational infrastructure shifts from public signals.

## When not to use

Illicit surveillance or harvesting non-public personal information (strictly prohibited by repo security MUST). Authoritative framework captures (use `reference-maintain`).

## Criticality

High: Strategic intelligence often leaks or appears in public PRs, model cards, public commit messages, and researcher forum threads well ahead of formal PR marketing.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. OSINT dossiers write under `results/research/community/osint/<entity>/<YYYY-MM-DD>/`.

## How to use

1. Formulate intelligence questions and search vectors:
   - Public repository commit messages and PR comments (GitHub/GitLab).
   - Package registry releases (PyPI, npm, crates.io).
   - Public statements and slides by lead researchers.
2. Cross-reference signals against multiple independent public sources.
3. Classify evidence confidence:
   - **Confirmed (P0)**: Public code commits, official changelogs, verifiable repository tags.
   - **Probable (P1)**: Multiple corroborating practitioner accounts with receipts.
   - **Hypothesis (P2)**: Single-source public claim without independent confirmation.
4. Synthesize OSINT timeline and structural findings into `results/research/community/osint/`.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill social-osint --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). No private PII, credentials, or confidential employee data in intelligence reports. Use only public, authorized data.

## Completion gates

Confirm structured OSINT briefing is written under `results/research/community/osint/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
