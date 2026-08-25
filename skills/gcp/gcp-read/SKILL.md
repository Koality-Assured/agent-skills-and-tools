---
name: gcp-read
description: >-
  Read-only GCP inventory/status via OAuth or named profiles; summarize into
  results/. Use when the human asks to inspect GCP without changes. Do not use
  for writes (gcp-write) or log deep-dives (gcp-logs).
owner_agent: cloud-operator
rank: medium
isolation: mutate
---

# GCP read

## When to use

Read-only GCP inspection via OAuth / named profiles; summarize under `results/`.

## When not to use

Mutating GCP (`gcp-write` — requires human-turn auth). Log analysis (`gcp-logs`). Committing credentials. Destructive changes without write skill + auth.

## Criticality

Medium: default for read; stop if credentials would need to be stored in-repo.

## Source of truth

- GCP CLI/SDK via OAuth or named profiles
- `python scripts/results/new_run_dir.py --family research --topic <slug>`
- [`ai-tooling/a2a/interaction-protocol.md`](../../../../ai-tooling/a2a/interaction-protocol.md)

## Isolation

`mutate` because summaries write `results/`. Parent spawns `cloud-operator` with area `results`.

## How to use

1. Confirm profile/OAuth is available; never store credentials in the repo.
2. Perform read-only GCP queries needed for the ask.
3. `python scripts/results/new_run_dir.py --family research --topic <slug>` then write the summary under that path; compress bulky JSON (Headroom).
4. Return paths + high-level findings — not full API dumps.

## Dry run

```bash
python scripts/results/new_run_dir.py --family research --topic <slug> --dry-run
```

Confirm profile exists and list intended read APIs without calling write APIs.

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Never commit creds/tokens. A2A MUST NOT destructive-delegate. For changes, require `gcp-write` + human-turn authorization.

## Completion gates

Summary path under `results/`. No credential material in return.
