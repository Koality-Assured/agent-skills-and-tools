---
schema_version: "2.0.0"
name: community-troubleshooting
description: >-
  Investigates and triages technical errors, obscure build failures, framework regressions,
  and library bugs by searching practitioner communities, Stack Overflow, GitHub Discussions,
  and subreddits. Use when facing undocumented exceptions, cryptic compiler errors, upstream
  SDK regressions, or environment-specific bugs with no official vendor solution. Do not use
  for standard code-review without error context (code-review-report).
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
      error_message:
        type: string
        description: Exact error message or stack trace
      framework:
        type: string
        description: Target framework or language (e.g. Python, Rust, Docker, PyTorch)
  outputs:
    task_id: string
    status: string
    artifacts: list
    handoff_requests: list
    metrics: dict
---

# Community troubleshooting

## When to use

Triaging cryptic technical errors, undocumented SDK bugs, breaking regressions in third-party libraries, and edge-case build errors by mining verified practitioner discussions across Stack Overflow, GitHub Issue trackers, Reddit (`r/rust`, `r/golang`, `r/devops`, `r/LocalLLaMA`), and Discourse developer forums.

## When not to use

Standard code-review without errors (use `code-review-report`). Adversarial system architecture review (use `antagonistic-review`). Model benchmark comparisons (use `benchlm-lookup`).

## Criticality

High: Unblocking development on cutting-edge or rapidly shifting toolchains often requires extracting crowd-sourced workarounds, patches, or environment flag overrides before official documentation is updated.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/community_analyzer.py`](../../../../scripts/research/community_analyzer.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Triage notes write under `results/research/community/troubleshooting/<topic>/<YYYY-MM-DD>/`.

## How to use

1. Locate top-tier practitioner communities for the relevant technology:
   ```bash
   python scripts/research/community_analyzer.py --topic devops --min-tier Tier 1
   ```
2. Search for exact error signatures, stripping user-specific file paths or hostnames.
3. Extract candidate workarounds, evaluating:
   - **Root Cause Hypothesis**: Why the regression or error occurs.
   - **Workaround Quality**: Non-destructive workaround vs. risky monkey-patch.
   - **Receipt Verification**: Confirm that the solution worked for multiple independent users.
4. Record findings and reproduction steps into `results/research/community/troubleshooting/`.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill community-troubleshooting --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Community workarounds must be vetted for malicious payload injection (e.g. `curl | sh` or unsafe deserialization) before application.

## Completion gates

Confirm structured troubleshooting triage is written under `results/research/community/troubleshooting/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
