---
name: downstream-repo-update
description: >-
  Ai-router-internal workflow for synchronized, sanitized publication to its public downstream repositories. Use when publishing from a full ai-router checkout. This skill is not supported in a standalone export; use the destination repository's own release and security procedures there.
owner_agent: harness-operator
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

This procedure is for the full ai-router checkout only. It requires private repository mappings and sanitization tooling that are not included in the standalone skills export. Standalone users must not invoke it or treat its commands as a publishing procedure; follow the destination repository's own release and security rules.

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

- `scripts/sync/sync_and_push_downstreams.py` (`../../../../scripts/sync/sync_and_push_downstreams.py`; ai-router-only, optional provenance)
- `scripts/sync/sync_public_repos.py` (`../../../../scripts/sync/sync_public_repos.py`; ai-router-only, optional provenance)
- `docs/agent-session-security.md` (`../../../../docs/agent-session-security.md`; ai-router-only, optional provenance)
- [`ai-tooling/skills/meta/sync-downstream-repos/SKILL.md`](../sync-downstream-repos/SKILL.md)
- [`ai-tooling/skills/meta/isolate-work/SKILL.md`](../isolate-work/SKILL.md)

## Isolation

`mutate`. Parent router isolates the session with `isolate-work` before spawning `repo-sync-ops`.

## How to use

1. Audit source directory coverage to ensure no new domain folders are unmapped:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --check-coverage
   ```
2. Run dry-run simulation to review planned file changes and redactions:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run
   ```
3. Inspect the generated redaction audit log. Ensure zero unintended leaks or schema violations.
4. Perform live export synchronization, commit, and remote push:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --message "feat: sync updates from ai-router" --push
   ```
   Or target a specific downstream repository:
   ```bash
   python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --repo agent-skills-and-tools --message "feat: sync skills" --push
   ```
5. Verify all 6 downstream repositories report `Status: success` or `Status: clean_up_to_date` and `(Pushed)`.

## Dry run

```bash
python scripts/sync/sync_and_push_downstreams.py --check-coverage
python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run
python scripts/sync/sync_and_push_downstreams.py --dest c:/Code --dry-run --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Follow destination-local security rules. In the full ai-router checkout, all public exports MUST use its sanitization engine in `sync_public_repos.py`; that private tool is not included in standalone exports. Never bypass redaction filters or commit live credentials or tokens into downstream destinations, and audit all redaction events.

## Completion gates

Verify publish summary table and confirm all repositories are clean and up to date with remote `origin/main`. Record change-history entry if material public exports were updated.
