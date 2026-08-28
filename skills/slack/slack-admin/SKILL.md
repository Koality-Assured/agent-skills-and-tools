---
name: slack-admin
description: >-
  Audit Slack workspace security configurations, Single Sign-On (SSO) enforcement, public channel sprawl, user role hierarchy, and compliance posture. Use when auditing Slack workspace security baselines, checking user roles, verifying app approval policies, or evaluating compliance for koality-assured or enterprise workspaces.
owner_agent: chat-collab-agent
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
  - Target workspace identifier (default koality-assured), audit scope, security compliance checklist
  outputs:
  - Workspace security audit report, violation inventory, role assignment summary under results/
topics: [slack, admin, security, audit, sso, compliance, governance]
routing_hints: [slack-admin, workspace-audit, audit-slack, slack-governance, sso-check, channel-audit]
---

# Slack workspace administration and security audit

Audit Slack workspace configurations, Single Sign-On policies, app governance, and compliance baselines.

## When to use

- Auditing workspace security posture against CIS Slack Benchmark controls.
- Inspecting Single Sign-On (SSO), Multi-Factor Authentication (MFA), and session lifetime settings.
- Checking workspace App Approval Mode and auditing installed integrations.
- Identifying inactive public channels, unmonitored private channels, and user role sprawl.
- Generating compliance and security audit reports for the `koality-assured` workspace.

## When not to use

- Routine message posting and notifications (use `slack-message`).
- Dispatching incoming webhook alerts (use `slack-webhook`).
- Creating and validating App Manifests (use `slack-app-manage`).
- Administering Google Workspace tenants (use `google-workspace-admin`).

## Criticality

High. Workspace administration audits evaluate organizational security perimeters, access controls, and compliance.

## Source of truth

- CLI tool: `scripts/slack/slack_admin.py`
- Admin standard: [`docs/standards/slack-interaction-and-administration.md`](../../../../docs/standards/slack-interaction-and-administration.md)
- Reference baseline: [`references/slack-security/slack-security-baseline.md`](../../../../references/slack-security/slack-security-baseline.md)

## Isolation

Mutating administrative changes run in an isolated worktree and require explicit human authorization in the current turn. Read-only compliance audits may run on primary.

## How to use

1. Run workspace security posture audit:
   ```bash
   python scripts/slack/slack_admin.py audit-workspace \
     --workspace koality-assured \
     --json
   ```
2. Audit channel governance and sprawl:
   ```bash
   python scripts/slack/slack_admin.py audit-channels \
     --workspace koality-assured \
     --json
   ```
3. Audit installed integrations and requested scopes:
   ```bash
   python scripts/slack/slack_admin.py audit-apps \
     --workspace koality-assured \
     --json
   ```

## Dry run

Execute simulated workspace audits without live API calls:
```bash
python scripts/slack/slack_admin.py audit-workspace \
  --workspace koality-assured \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never store or commit Slack admin tokens (`xoxp-`, `xoxb-`). All audit results must sanitize PII and secret tokens.

## Completion gates

- Security audit executes and produces a structured findings report.
- Report artifacts saved to `results/`.
- No sensitive user tokens or unredacted secrets emitted.
