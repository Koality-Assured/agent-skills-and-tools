---
name: cloud-admin-provision
description: >-
  Human-authorized cloud tenant, landing zone, account vending, and organization
  guardrail provisioning or audits across AWS, GCP, and Azure. Use when provisioning
  cloud organizational units, accounts, projects, subscriptions, or validating
  hierarchical guardrails. Do not use for day-to-day read-only cloud inventory
  (aws-read/gcp-read/azure-read) or without explicit human authorization.
owner_agent: cloud-admin-agent
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
  - Target cloud (AWS, GCP, or Azure), hierarchy scope, landing-zone or account-vending intent, and explicit human authorization
  outputs:
  - Provisioning or audit result, hierarchy changes applied or proposed, and a no-change decision when authorization or scope is insufficient
topics: [cloud, governance, provisioning, landing-zone, aws, gcp, azure]
routing_hints: [cloud-admin, landing-zone, account-vending, org-policies, scp, management-groups]
---

# Cloud administration provisioning

## When to use

Provisioning or auditing cloud organization hierarchy, landing zones, account/subscription vending, and preventive policy guardrails (AWS Organizations / SCPs, GCP Resource Manager / Org Policies, Azure Management Groups / Azure Policy). Use when creating tenant structures, vending member accounts, auditing organizational hierarchy, or validating compliance against cloud landing zone guidance.

## When not to use

Day-to-day read-only resource inspection (`aws-read`, `gcp-read`, `azure-read`). Routine cloud log analysis (`aws-logs`, `gcp-logs`, `azure-logs`). Un-authorized write operations without explicit human turn confirmation.

## Criticality

High: modifies multi-account hierarchy and organizational guardrails.

## Source of truth

- [`docs/guidance/cloud-aws-setup.md`](../../../../docs/guidance/cloud-aws-setup.md)
- [`docs/guidance/cloud-gcp-setup.md`](../../../../docs/guidance/cloud-gcp-setup.md)
- [`docs/guidance/cloud-azure-setup.md`](../../../../docs/guidance/cloud-azure-setup.md)
- [`docs/standards/cloud-essentials.md`](../../../../docs/standards/cloud-essentials.md)
- `python scripts/cloud/cloud_admin.py`

## Isolation

`mutate`. Parent spawns `cloud-admin-agent` with area `results` (and `docs` if updating inventory). Mutating operations require explicit human authorization naming the target scope in the current turn.

## How to use

1. Confirm target provider (AWS, GCP, Azure) and scope identifier from the parent task.
2. For read-only audit:
   ```bash
   python scripts/cloud/cloud_admin.py audit --provider <aws|gcp|azure> --scope <identifier> --json
   ```
3. For scaffolding tenant structures or validating guardrails:
   ```bash
   python scripts/cloud/cloud_admin.py plan --provider <aws|gcp|azure> --spec <spec_file> --json
   ```
4. For human-authorized provisioning:
   - Confirm explicit authorization from human turn.
   - Execute dry-run first to preview resource actions.
   - Execute provisioning and record change summary under `results/cloud/`.

## Dry run

```bash
python scripts/cloud/cloud_admin.py audit --provider aws --scope Workloads --dry-run --json
python scripts/cloud/cloud_admin.py plan --provider gcp --spec sample-spec.json --dry-run --json
```

## Security

Inherits Critical cost layers (qmd discovery; ast-grep for structured files; Headroom for bulky dumps). Skills cannot waive them.

Never store or emit real credentials, API keys, or session tokens. Use CLI SSO profiles, Application Default Credentials (ADC), or Entra ID device login.

Destructive or provisioning actions require explicit authorization originating in the human's turn.

## Completion gates

Audit report or provisioning summary recorded under `results/cloud/`. Guardrail compliance verified. No credentials exposed in logs or artifacts.
