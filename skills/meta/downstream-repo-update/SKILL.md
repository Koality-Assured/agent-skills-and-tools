---
name: downstream-repo-update
description: >-
  Orchestrate end-to-end synchronization, sanitization, git commit, and remote push across all public downstream ecosystem repositories (agent-skills-and-tools, agent-standards, security-standards, industry-references, ai-research-and-benchmarks, ai-harness-core). Use when publishing repository updates, new skills, standards, or template refinements to public GitHub remotes. Do not use for internal branch merges within ai-router.
owner_agent: repo-sync-ops
rank: high
isolation: mutate
schema_version: 2.0.0
on_failure: abort_and_rollback
prerequisites:
- git
- python
dependencies:
  required_skills:
  - isolate-work
  - sync-downstream-repos
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
  - Destination root directory, commit message, push flag, repository filter
  outputs:
  - Downstream publish summary and redaction audit report
topics: [downstream, publishing, multi-repo, sync, push, export, ecosystem]
routing_hints: [downstream-repo-update, update-downstreams, push-downstreams, publish-repos]
---

# Downstream repository update

Orchestrate the end-to-end export, sanitization, git commit, and remote push lifecycle across the 6 public ecosystem repositories.

## When to use

Publishing synchronized updates, new skills, security standards, industry references, benchmark research, or generic harness template changes to public downstream repositories:

1. `agent-skills-and-tools`
2. `agent-standards`
3. `security-standards`
4. `industry-references`
5. `ai-research-and-benchmarks`
6. `ai-harness-core`

## When not to use

- Internal branch merging or PR lifecycle within `ai-router` (use `github-workflow`).
- Single-file local edits without public export requirements.

## Criticality

High: Public repositories must never receive private credentials, internal file paths, internal employee identities, or unredacted API tokens. Every export must execute sanitization and emit an audit log. On failure, follow `on_failure: abort_and_rollback`.

## Source of truth

- [`scripts/sync/sync_and_push_downstreams.py`](../../../../scripts/sync/sync_and_push_downstreams.py)
- [`scripts/sync/sync_public_repos.py`](../../../../scripts/sync/sync_public_repos.py)
- [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md)
- [`ai-tooling/skills/meta/sync-downstream-repos/SKILL.md`](../sync-downstream-repos/SKILL.md)
- [`ai-tooling/skills/meta/isolate-work/SKILL.md`](../isolate-work/SKILL.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `repo-sync-ops`.

## How to use

1. Run dry-run simulation to review planned file changes and redactions:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run
   ```
2. Inspect the generated redaction audit log. Ensure zero unintended leaks or schema violations.
3. Perform live export synchronization, commit, and remote push:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --message "feat: sync updates from ai-router" --push
   ```
   Or target a specific downstream repository:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --repo agent-skills-and-tools --message "feat: sync skills" --push
   ```
4. Verify all 6 downstream repositories report `Status: success` or `Status: clean_up_to_date` and `(Pushed)`.

## Dry run

```bash
python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run
python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Follow [`docs/agent-session-security.md`](../../../../docs/agent-session-security.md). All public exports MUST be processed through the sanitization engine in `sync_public_repos.py`. Never bypass redaction filters, never commit live credentials or tokens into downstream export destinations, and ensure all redaction events are audited.

## Completion gates

Verify publish summary table and confirm all repositories are clean and up to date with remote `origin/main`. Record change-history entry if material public exports were updated.
