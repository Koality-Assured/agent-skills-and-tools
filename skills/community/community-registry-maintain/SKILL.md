---
schema_version: "2.0.0"
name: community-registry-maintain
description: >-
  Audits, scores, updates, and maintains the community reliability catalog and rubric under
  references/socials/. Use when adding new developer forums or subreddits, recalculating
  community reliability scores, auditing signal drift, or validating the social registry
  against schema rules. Do not use for standard reference framework maintenance (reference-maintain).
owner_agent: community-analyst
rank: high
isolation: mutate
on_failure: abort_and_rollback
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
      action:
        type: string
        enum: [validate, add, rescore, audit]
      community_id:
        type: string
  outputs:
    task_id: string
    status: string
    artifacts: list
    handoff_requests: list
    metrics: dict
---

# Community registry maintain

## When to use

Adding new developer forums, subreddits, or technical platforms to `references/socials/catalogs/ranked-communities.json`, scoring candidate communities against the 6-dimension reliability rubric, auditing existing communities for signal degradation/moderation drift, and validating JSON catalog integrity.

## When not to use

Capturing official NIST/MITRE/OWASP frameworks (use `reference-maintain`). General documentation authoring (use `doc-builder`). Running community research queries (use `community-analyzer` CLI).

## Criticality

High: Maintains the integrity and reliability ratings of external community discovery channels, ensuring agents prioritize high-signal practitioner sources over low-signal or astroturfed forums.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/manage_social_registry.py`](../../../../scripts/research/manage_social_registry.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Edits land directly on `references/socials/`.

## How to use

1. Validate existing catalog integrity:
   ```bash
   python scripts/research/manage_social_registry.py --validate
   ```
2. Score a candidate community against the 6 rubric dimensions:
   - Technical Depth (0–20)
   - Moderation Rigor (0–20)
   - Citation Standard (0–20)
   - Vendor Resistance (0–15)
   - Signal-to-Noise (0–15)
   - Reproducibility (0–10)
   ```bash
   python scripts/research/manage_social_registry.py --score 18 16 18 12 14 8
   ```
3. Update `references/socials/catalogs/ranked-communities.json` and associated dossier pages (`technical-subreddits.md` or `developer-forums.md`).
4. Re-run validation to ensure clean tier alignment and schema compliance.

## Dry run

```bash
python scripts/research/manage_social_registry.py --validate
python scripts/ai-tooling/validate_skill.py --skill community-registry-maintain --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Community catalog URLs must be validated HTTPS endpoints; no unauthorized or malicious endpoints.

## Completion gates

Confirm catalog passes `manage_social_registry.py --validate`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`). Append change history.
