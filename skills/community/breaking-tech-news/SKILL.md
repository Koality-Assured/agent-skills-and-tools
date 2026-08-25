---
schema_version: "2.0.0"
name: breaking-tech-news
description: >-
  Monitors and synthesizes breaking technical news, critical zero-day disclosures, major
  security breaches, and frontier AI model weight releases from fast-moving social feeds and
  community alerts. Use when checking for immediate breaking security advisories, high-severity
  vulnerabilities, or unannounced frontier AI model drops. Do not use for scheduled weekly vendor
  briefings (ai-vendor-updates).
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
    - News domain focus (security, ai, cloud, or all) and urgency threshold
  outputs:
    - Breaking-event briefing with source links, severity notes, and follow-up caveats
---

# Breaking tech news

## When to use

Tracking, capturing, and synthesizing urgent breaking technical events: critical 0-day vulnerabilities, active supply-chain compromises (e.g. PyPI/npm malware campaigns), sudden major cloud service degradations, and unexpected frontier model drops announced via fast-moving channels (`r/netsec`, `r/LocalLLaMA`, X/Twitter researcher alerts, Hacker News).

## When not to use

Scheduled weekly frontier AI updates (use `ai-vendor-updates`). In-depth vulnerability mitigation reports (use `threat-model` or `code-review-report`). Standard benchmark lookups (use `benchlm-lookup`).

## Criticality

High: Rapid awareness of zero-day exploits and supply chain attacks allows immediate defensive posture adjustments before official vendor patches or advisory feeds update.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/community_analyzer.py`](../../../../scripts/research/community_analyzer.py)
- [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Breaking news briefs write under `results/reports/breaking-news/<YYYY-MM-DD>/`.

## How to use

1. Query high-urgency Tier 0 channels:
   ```bash
   python scripts/research/community_analyzer.py --topic security --min-tier Tier 0
   ```
2. Filter for verified critical alerts, classifying by:
   - **Urgency Tier**: Critical (active exploitation / immediate action), High (major release / impending deprecation), Moderate.
   - **Impact Scope**: Affected libraries, cloud providers, model weights, or operating systems.
   - **Immediate Mitigation**: Temporary configuration flags, package version pins, or firewall rules.
3. Emit flash alert under `results/reports/breaking-news/`.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill breaking-tech-news --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Breaking news feeds often carry panic-driven misinformation; verify exploit receipts before issuing critical alerts.

## Completion gates

Confirm structured flash news report is written under `results/reports/breaking-news/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
