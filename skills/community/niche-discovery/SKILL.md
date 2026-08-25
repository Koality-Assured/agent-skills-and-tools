---
schema_version: "2.0.0"
name: niche-discovery
description: >-
  Discovers niche tools, specialized boutique libraries, obscure scripts, and cutting-edge
  community implementations discussed in specialized forums and technical subreddits. Use when
  looking for lesser-known alternatives, boutique quantization kernels, specialized agent
  frameworks, or innovative community hacks. Do not use for mainstream vendor evaluations
  (ai-vendor-updates).
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
    - Capability domain and license, runtime, or language constraints
  outputs:
    - Niche tool or library candidates with community provenance and constraint fit
---

# Niche discovery

## When to use

Finding specialized open-source libraries, boutique tools, undocumented optimizations, custom inference kernels (e.g. FlashMLA, BitNet, AWQ kernels), and indie developer projects discussed across specialized subreddits (`r/LocalLLaMA`, `r/Compilers`, `r/ReverseEngineering`), Hacker News `Show HN`, and GitHub repositories.

## When not to use

Mainstream frontier AI vendor updates (use `ai-vendor-updates`). Standard model benchmark leaderboard lookups (use `benchlm-lookup`). General documentation writing (use `doc-builder`).

## Criticality

High: Rapid innovation in AI and developer tooling often originates in indie and open-source communities months before commercialization. Discovering niche tools provides significant technical and architectural leverage.

## Source of truth

- [`references/socials/community-reliability-rubric.md`](../../../../references/socials/community-reliability-rubric.md)
- [`references/socials/catalogs/ranked-communities.json`](../../../../references/socials/catalogs/ranked-communities.json)
- [`scripts/research/community_analyzer.py`](../../../../scripts/research/community_analyzer.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `community-analyst`. Discovery dossiers write under `results/research/community/niche-discovery/<domain>/<YYYY-MM-DD>/`.

## How to use

1. Query Tier 0 and Tier 1 niche communities:
   ```bash
   python scripts/research/community_analyzer.py --topic ai --min-tier Tier 0
   ```
2. Scan for boutique solutions, evaluating:
   - **Utility & Distinctiveness**: What unique problem does this tool solve?
   - **Code Quality & Activity**: Repository commit frequency, license, and issue activity.
   - **Community Endorsement**: Practical adoption by recognized practitioners vs. self-promotion spam.
3. Formulate comparative dossier with links, reproduction instructions, and performance notes.

## Dry run

```bash
python scripts/research/community_analyzer.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill niche-discovery --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). Niche repositories must be audited for supply-chain risk and malicious code before importing into production codebases.

## Completion gates

Confirm structured niche discovery dossier is written under `results/research/community/niche-discovery/`. Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`).
