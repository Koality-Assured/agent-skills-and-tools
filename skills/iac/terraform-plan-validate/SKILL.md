---
schema_version: "2.0.0"
name: terraform-plan-validate
description: >-
  Validate Terraform and OpenTofu configurations, check formatting, run linting,
  and generate speculative execution plans without mutating infrastructure. Use
  when verifying syntax, validating HCL configurations, checking module compatibility,
  or producing plan diffs. Do not use for applying changes to live environments or modifying files.
owner_agent: as-code-agent
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - git
  - python
  - terraform
dependencies:
  required_skills: []
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    - Path to Terraform configuration directory or root module
    - Target environment parameters, variable definitions (.tfvars), or backend configurations
  outputs:
    - Validation and linting report detailing fmt, validate, and tflint diagnostic results
    - Speculative execution plan summary and structured plan output path (e.g. plan.json)
topics: [terraform, opentofu, iac, validation, plan, lint]
routing_hints: [terraform-plan, terraform-validate, tfplan, tflint, iac-validation, plan-diff]
---

# Terraform plan and validate

## When to use

Validate Terraform and OpenTofu syntax, check formatting consistency, run provider schema validations, and generate speculative execution plans (`tfplan` / `plan.json`) for review without modifying real cloud infrastructure. Use when reviewing proposed IaC changes, verifying pull requests, or confirming that configuration files match provider expectations.

## When not to use

Authoring or refactoring Terraform module structures (`terraform-module-builder`). Running static security and compliance policy scans (`iac-security-audit`). Applying or mutating real cloud resources (handled via human-confirmed cloud operator workflows; never automated via A2A).

## Criticality

High: ensures that configurations are syntactically and structurally sound before changes reach deployment pipelines. Never execute mutating `apply` actions within this skill.

## Source of truth

- ai-router-only sources: `supporting/terraform/cli-workflow.md`, `supporting/terraform/module-patterns.md`, `supporting/terraform/state-management.md`, and `docs/standards/cloud-essentials.md`
- Standalone repositories should follow their local change-control and security rules and current official provider documentation.

## Isolation

Standalone dispatch: Follow the destination's isolation and dispatch rules. Use a registered local operator or continue in-session when those rules permit; report a capability gap if no local path supports the work.

`read-only`. In ai-router, the parent spawns `as-code-agent` with area `results`. This skill executes in read-only mode and produces validation artifacts and plan inspection outputs without altering workspace files or remote infrastructure state.

## How to use

1. Confirm target configuration directory and environment variable parameters from the parent task.
2. Execute formatting check:
   ```bash
   terraform fmt -check -diff -recursive <target_dir>
   ```
3. Initialize the working directory in read-only/speculative mode:
   ```bash
   terraform init -backend=false
   ```
4. Validate internal syntax and provider schema definitions:
   ```bash
   terraform validate -json
   ```
5. If remote state and credentials are configured in a designated test/staging environment, generate a speculative plan:
   ```bash
   terraform plan -input=false -detailed-exitcode -out=tfplan
   terraform show -json tfplan > plan.json
   ```
6. Parse and extract key plan metrics (resources to add, change, or destroy).
7. Format findings into a structured validation summary report.

## Dry run

Execute `terraform fmt -check` and `terraform validate` against local configuration directories. For environments with mock or local backends, run `terraform plan` with `-refresh=false` to verify plan generation logic without remote network queries.

## Security

Inherits Critical cost layers in ai-router (qmd discovery; ast-grep for structured files; Headroom for bulky dumps). Standalone repositories follow their destination root `AGENTS.md` and tooling requirements.

A2A MUST NOT apply or deploy changes to real clouds. Never emit unmasked secrets, database credentials, or private keys in terminal output or saved plan artifacts. Inspect plan JSON outputs with filters that redact sensitive attributes.

## Completion gates

Validation report detailing `fmt`, `validate`, and plan status. Confirm that no cloud resources were mutated and no state locks were left dangling.
