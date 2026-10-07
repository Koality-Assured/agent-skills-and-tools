---
schema_version: "2.0.0"
name: terraform-module-builder
description: >-
  Author, scaffold, and refactor standard Terraform and OpenTofu modules, complete
  with variable validations, sensitive outputs, dynamic blocks, and versions.tf.
  Use when generating reusable infrastructure modules, scaffolding cloud components,
  or refactoring existing HCL modules under results/as-code/ or workspace paths.
  Do not use for applying infrastructure changes to live cloud environments.
owner_agent: as-code-agent
rank: high
isolation: mutate
on_failure: abort_and_rollback
prerequisites:
  - git
  - python
  - terraform
dependencies:
  required_skills:
    - isolate-work
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    - Module name, target cloud provider (AWS/Azure/GCP), resource architecture specifications, and target directory
  outputs:
    - Scaffolded Terraform module files (main.tf, variables.tf, outputs.tf, versions.tf, README.md, terraform.tfvars.example)
    - Syntax formatting verification and local dry-run validation logs
topics: [terraform, opentofu, iac, modules, scaffolding, hcl]
routing_hints: [terraform-module, module-builder, terraform-scaffold, hcl-authoring, module-pattern]
---

# Terraform module builder

## When to use

Authoring new reusable Terraform/OpenTofu modules or refactoring existing modules to meet repository standards. Use when generating standard module anatomy (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`, `terraform.tfvars.example`), embedding input validation blocks, configuring sensitive outputs, implementing `for_each` idioms, and parameterizing dynamic resource blocks.

## When not to use

Validating existing configurations without modifying files (`terraform-plan-validate`). Conducting static security and policy audits (`iac-security-audit`). Executing live infrastructure deployments to cloud providers.

## Criticality

High: generates reusable infrastructure building blocks that directly dictate security, scalability, and maintainability across stacks. Modules must adhere to strict type validation and security standards.

## Source of truth

- ai-router-only sources: `supporting/terraform/module-patterns.md`, `supporting/terraform/cli-workflow.md`, and `supporting/terraform/security-hardening.md`
- Standalone repositories should use their local module patterns and current official Terraform/OpenTofu provider documentation.
- ai-router-only output helper: `python scripts/results/new_run_dir.py --family as-code --topic <slug> --type terraform`

## Isolation

Standalone dispatch: Follow the destination's isolation and dispatch rules. Use a registered local operator or continue in-session when those rules permit; report a capability gap if no local path supports the work.

`mutate`. In ai-router, the parent spawns `as-code-agent` with area `results` (or the relevant worktree if authoring repository modules). Worktree isolation is required before mutating files.

## How to use

1. Confirm module requirements, resource scope, and target cloud provider from parent task.
2. Choose an output directory under `results/as-code/terraform/<topic>/<YYYY-MM-DD>/` in ai-router, or use the destination repository's module/output convention. In ai-router, initialize it with:
   ```bash
   python scripts/results/new_run_dir.py --family as-code --topic <topic> --type terraform
   ```
3. Author standard module anatomy files:
   - `versions.tf`: Declare minimum required Terraform version and provider constraints with optimistic pessimistic operators (`~> 5.0`).
   - `variables.tf`: Declare strongly typed input variables with descriptive text and `validation` blocks.
   - `main.tf`: Declare resource blocks, data sources, and `locals {}`. Use `for_each` over `count` for stable resource addressing.
   - `outputs.tf`: Declare outputs, marking sensitive values with `sensitive = true`.
   - `README.md`: Document module usage, requirements, inputs, outputs, and an example declaration.
   - `terraform.tfvars.example`: Provide sample input assignments.
4. Format all HCL files:
   ```bash
   terraform fmt -recursive <module_dir>
   ```
5. Validate configuration syntax:
   ```bash
   terraform -chdir=<module_dir> init -backend=false
   terraform -chdir=<module_dir> validate
   ```

## Dry run

In ai-router, preview directory scaffolding with the local helper:
```bash
python scripts/results/new_run_dir.py --family as-code --topic <topic> --type terraform --dry-run
```

In any repository with Terraform installed, run `terraform fmt -check <module_dir>`. Standalone repositories should use their local output convention and available Terraform checks.

## Security

Inherits Critical cost layers in ai-router (qmd discovery; ast-grep for structured files; Headroom for bulky dumps). Standalone repositories follow their destination root `AGENTS.md` and tooling requirements.

A2A MUST NOT apply or deploy changes to real clouds. Never hardcode credentials, access keys, or unmasked secrets in module defaults or examples. Enforce default encryption (KMS CMK) and private network isolation on created resources.

## Completion gates

Validated module directory containing `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, and `README.md`. `terraform fmt -check` and `terraform validate` must pass cleanly with zero errors. Confirm nothing was applied to live clouds.
