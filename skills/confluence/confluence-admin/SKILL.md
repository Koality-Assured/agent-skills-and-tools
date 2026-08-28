---
name: confluence-admin
description: >-
  Audit, configure, and govern Confluence space permissions, page restrictions, user access, space export, retention, and compliance policies. Use when auditing space security postures, inspecting page access restrictions, reviewing permission matrices, or exporting space archives.
owner_agent: docs-collab-agent
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
  - Target workspace (default koality-assured), space key, audit criteria, export format (HTML/XML/PDF)
  - Explicit human authorization for mutating workspace-wide permissions or deleting spaces
  outputs:
  - Space security audit reports, restriction matrices, export job IDs, and compliance summaries under results/
topics: [confluence, admin, permissions, security, governance, audit]
routing_hints: [confluence-admin, audit-space-permissions, page-restrictions, space-export, confluence-governance]
---

# Confluence space administration and governance

Audit and administer Confluence spaces, permissions, page restrictions, and compliance baselines.

## When to use

- Auditing space permissions and access matrices across groups and individual accounts.
- Inspecting page-level view and edit restrictions.
- Verifying least-privilege access for guest users and external collaborators.
- Initiating and monitoring space exports for archival or backup purposes.
- Evaluating workspace compliance against data retention policies.

## When not to use

- Publishing or updating page content (use `confluence-doc-manage`).
- Developing or packaging Forge applications (use `confluence-app-manage`).
- Subscribing to or validating webhook events (use `confluence-webhook`).
- Administering Slack workspaces or SSO (use `slack-admin`).

## Criticality

High. Space permissions and restrictions enforce confidentiality boundaries across organizational teams.

## Source of truth

- CLI tool: `scripts/confluence/confluence_admin.py`
- Administration standard: [`docs/standards/confluence-interaction-and-administration.md`](../../../../docs/standards/confluence-interaction-and-administration.md)
- SaaS security standard: [`docs/standards/saas-security.md`](../../../../docs/standards/saas-security.md)
- Workspace governance guide: [`docs/guidance/confluence-workspace-and-page-governance.md`](../../../../docs/guidance/confluence-workspace-and-page-governance.md)

## Isolation

Mutating space permissions, granting admin roles, or deleting spaces MUST run in the worktree the parent spawned and MUST halt unless the **human's own message** in the current turn explicitly authorizes it. Read-only audits may run on primary.

## How to use

1. Audit space security posture and permission matrices:
   ```bash
   python scripts/confluence/confluence_admin.py audit-space \
     --workspace koality-assured \
     --space-key "ENG" \
     --json
   ```
2. Inspect page-level restrictions across a space:
   ```bash
   python scripts/confluence/confluence_admin.py check-restrictions \
     --workspace koality-assured \
     --space-key "ENG" \
     --json
   ```
3. Export space content for backup or compliance:
   ```bash
   python scripts/confluence/confluence_admin.py export-space \
     --workspace koality-assured \
     --space-key "ENG" \
     --format "pdf" \
     --dry-run \
     --json
   ```

## Dry run

Run permission audits and export validations without live modifications:
```bash
python scripts/confluence/confluence_admin.py audit-space \
  --workspace koality-assured \
  --space-key "ENG" \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never hardcode or expose admin API tokens. Use `CONFLUENCE_API_TOKEN` and `CONFLUENCE_EMAIL`.

Modifying global space permissions or removing access policies requires explicit human authorization in the immediate turn.

## Completion gates

- Space audit or restriction inspection completed with clear findings.
- Identified security gaps (e.g. public anonymous write access) flagged.
- Audit summaries written cleanly under `results/`.
