---
name: google-drive-manage
description: >-
  Search Google Drive in bulk, create new files from results, update existing files on change, synchronize corpus materials down, and validate formatting and cleanliness. Use when creating files in Drive, searching Drive files in bulk, updating associated Drive documents, or synchronizing materials down to the local corpus. Do not use for domain-level Workspace admin settings (google-workspace-admin) or Gmail operations (google-gmail-manage).
owner_agent: google-suite-operator
rank: high
isolation: mutate
schema_version: 2.0.0
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
  - Drive folder ID or search query, source content, target destination, action (create/update/search/sync/validate)
  outputs:
  - Created or updated Drive file IDs, synchronized markdown corpus paths, validation summaries under results/
topics: [google, drive, docs, synchronization, validation]
routing_hints: [google-drive, drive-search, sync-corpus, file-creation, drive-validate]
---

# Google Drive manage

Search Google Drive in bulk, create and update files, synchronize corpus documents, and validate formatting and cleanliness.

## When to use

- Searching Drive files or folders in bulk with query filters.
- Creating new Google Docs, Sheets, or Drive files based on generated results.
- Updating existing Drive files when associated local resources or specs change.
- Synchronizing corpus materials down from Google Drive into local repository documentation.
- Validating that created or synchronized files are properly formatted, clean, and free of structural anomalies.

## When not to use

- Google Workspace domain administration and OU hierarchy (use `google-workspace-admin`).
- Gmail drafting or email operations (use `google-gmail-manage`).
- General cloud infrastructure provisioning (use `cloud-operator` / `cloud-admin-agent`).

## Criticality

High. File creation and corpus synchronization directly impact documentation accuracy and shared team resources.

## Source of truth

- Tooling CLI: `scripts/google/google_suite_ops.py`
- Interaction Standard: [`docs/standards/google-suite-interaction-and-administration.md`](../../../../docs/standards/google-suite-interaction-and-administration.md)
- Reference Security: [`references/google-workspace-security/drive-docs-security.md`](../../../../references/google-workspace-security/drive-docs-security.md)

## Isolation

Mutating operations run in an isolated worktree spawned by the parent coordinator. Read-only queries may run on primary.

## How to use

1. Discover relevant Google Suite standards using `qmd search "google drive sync standards"`.
2. For Drive search in bulk:
   ```bash
   python scripts/google/google_suite_ops.py drive search --query "type:document after:2026-08-01" --json
   ```
3. For file creation from local result:
   ```bash
   python scripts/google/google_suite_ops.py drive create --name "Report-Q3" --file "results/reports/report.md" --folder "[REDACTED_GOOGLE_DRIVE_TEST_FOLDER]"
   ```
4. For file validation (checking clean headings, frontmatter, and no corruptions):
   ```bash
   python scripts/google/google_suite_ops.py drive validate --file "docs/standards/google-suite-interaction-and-administration.md"
   ```
5. For corpus synchronization from Drive source:
   ```bash
   python scripts/google/google_suite_ops.py drive sync --source-id "[REDACTED_GOOGLE_DRIVE_TEST_FOLDER]" --dest "docs/standards/"
   ```

## Dry run

Verify CLI readiness and execute simulated Drive operations:
```bash
python scripts/google/google_suite_ops.py drive search --dry-run
python scripts/google/google_suite_ops.py drive validate --file "docs/standards/context-management.md" --dry-run
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never commit Google OAuth tokens or service account private keys. Testing Drive folder IDs ([REDACTED_GOOGLE_DRIVE_TEST_FOLDER]) are sanitized automatically upon public export.

## Completion gates

- Drive operations complete with exit code 0.
- Synchronized corpus documents pass markdown structural validation (`python scripts/docs/validate_structure_fast.py`).
- Results and audit logs recorded under `results/`.
