---
name: google-workspace-metadata
description: >-
  Collect cross-service metadata across Google Drive, Gmail, Docs, Users, Calendar, and Contacts. Use when inspecting metadata, permissions, resource relationships, or entity schemas across Google Suite. Do not use for file mutations (google-drive-manage) or domain admin policy enforcement (google-workspace-admin).
owner_agent: google-suite-operator
rank: medium
isolation: read-only
schema_version: 2.0.0
on_failure: abort_and_rollback
prerequisites:
- python
dependencies:
  required_skills: []
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
  - Target entity type (drive, gmail, users, calendar, contacts), scope identifier, field mask
  outputs:
  - Normalized JSON metadata schema and inventory reports under results/
topics: [google, metadata, inventory, schema, permissions]
routing_hints: [google-metadata, workspace-metadata, drive-metadata, user-metadata, permissions-audit]
---

# Google Workspace metadata

Universal metadata collector and inventory inspector across Google Workspace products.

## When to use

- Collecting comprehensive metadata from Drive files (owner, sharing perimeters, permissions, revisions).
- Inspecting Gmail thread metadata, label hierarchies, and participant lists.
- Auditing Google Calendar event attendees, recurrence rules, and conference links.
- Querying User profile metadata and organizational role attributes.

## When not to use

- Mutating files or uploading content (use `google-drive-manage`).
- Sending or drafting emails (use `google-gmail-manage`).
- Modifying domain organizational unit policies (use `google-workspace-admin`).

## Criticality

Medium. Read-only telemetry and metadata inspection.

## Source of truth

- Tooling CLI: `scripts/google/google_suite_ops.py`
- Security Reference: [`references/google-workspace-security/workspace-admin-security.md`](../../../../references/google-workspace-security/workspace-admin-security.md)

## Isolation

Read-only inspection. Safe to execute on primary checkout.

## How to use

1. Discover metadata schemas via `qmd search "google workspace metadata schemas"`.
2. Collect metadata across specific entities:
   ```bash
   python scripts/google/google_suite_ops.py metadata collect --service drive --target-id "[REDACTED_GOOGLE_DRIVE_TEST_FOLDER]" --json
   python scripts/google/google_suite_ops.py metadata collect --service user --target-id "developer@example.com" --json
   ```
3. Generate cross-service inventory summary:
   ```bash
   python scripts/google/google_suite_ops.py metadata collect --service all --scope "domain" --json
   ```

## Dry run

Execute simulated metadata collection:
```bash
python scripts/google/google_suite_ops.py metadata collect --service all --dry-run
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Ensure all collected metadata is sanitized of sensitive PII or session tokens before persistence in `results/`.

## Completion gates

- Metadata output formatted as normalized JSON.
- Output written under `results/` with zero credential leaks.
