---
name: google-workspace-admin
description: >-
  Google Workspace domain administration, organizational units (OUs), license management, 2FA/SSO enforcement, DLP, Zero Data Retention (ZDR), and external sharing audits. Use when auditing Workspace domain settings, managing OU policies, verifying ZDR/DLP compliance, or checking license allocation. Do not use for day-to-day user email/drive interactions (google-drive-manage/google-gmail-manage).
owner_agent: google-suite-admin
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
  - Domain name, target OU, audit scope, policy spec, explicit human authorization for modifications
  outputs:
  - Domain compliance audit reports, license usage matrices, and OU hierarchy trees under results/
topics: [google, admin, workspace, security, dlp, zdr, governance]
routing_hints: [google-admin, workspace-admin, ou-hierarchy, dlp-rules, zdr-compliance, license-audit]
---

# Google Workspace administration

Google Workspace tenant administration, organizational unit governance, license management, and security posture enforcement.

## When to use

- Auditing Google Workspace domain security settings, IdP SSO, and 2FA enforcement.
- Inspecting and managing Organizational Unit (OU) structure and policy inheritance.
- Validating Zero Data Retention (ZDR) and AI data governance settings.
- Auditing Data Loss Prevention (DLP) rules and external Drive/Gmail sharing perimeters.
- Auditing license assignment, unassigned seat costs, and product SKUs.

## When not to use

- Day-to-day file editing or corpus syncing (use `google-drive-manage`).
- Routine email drafting and sending (use `google-gmail-manage`).
- Public LLM API key management outside Workspace (use `public-llm-admin`).

## Criticality

High. Administrative modifications impact organization-wide security perimeters, authentication, and data compliance.

## Source of truth

- Administration CLI: `scripts/google/google_suite_admin.py`
- Interaction & Admin Standard: [`docs/standards/google-suite-interaction-and-administration.md`](../../../../docs/standards/google-suite-interaction-and-administration.md)
- Reference Security: [`references/google-workspace-security/workspace-admin-security.md`](../../../../references/google-workspace-security/workspace-admin-security.md)

## Isolation

Mutating domain changes run in an isolated worktree and require explicit human authorization in the current turn. Read-only compliance audits may run on primary.

## How to use

1. Discover admin standards using `qmd search "google workspace admin security baseline"`.
2. Run domain security audit:
   ```bash
   python scripts/google/google_suite_admin.py audit-domain --domain "example.com" --json
   ```
3. Audit license consumption and unassigned seats:
   ```bash
   python scripts/google/google_suite_admin.py audit-licenses --domain "example.com" --json
   ```
4. Audit OU hierarchy and DLP rules:
   ```bash
   python scripts/google/google_suite_admin.py audit-domain --domain "example.com" --check-dlp --check-zdr
   ```

## Dry run

Execute simulated domain audits:
```bash
python scripts/google/google_suite_admin.py audit-domain --domain "example.com" --dry-run
python scripts/google/google_suite_admin.py audit-licenses --domain "example.com" --dry-run
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never store or commit super-admin credentials, service account keys, or OAuth client secrets. All policy changes require explicit human-turn authorization.

## Completion gates

- Domain audits pass with complete findings summary.
- Audit artifacts saved to `results/`.
- No unredacted admin credentials or private directory paths emitted.
