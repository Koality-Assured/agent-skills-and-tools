---
schema_version: "2.0.0"
name: iac-security-audit
description: >-
  Audit Infrastructure-as-Code (Terraform, OpenTofu, CloudFormation) configurations
  for security misconfigurations, compliance violations, unencrypted resources, and IAM over-privilege.
  Use when scanning IaC manifests with Checkov, tfsec, Trivy, or TFLint before deployment
  or during pull-request reviews. Do not use for mutating IaC files or applying cloud changes.
owner_agent: as-code-agent
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - git
  - python
  - checkov
dependencies:
  required_skills: []
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    - Path to IaC manifests or repository directory to audit
    - Security baseline standards (e.g. CIS, NIST, AWS Foundational) and scan severity filters
  outputs:
    - Structured security audit report categorizing findings by severity, rule ID (e.g. CKV_AWS_...), and resource address
    - Actionable remediation recommendations and policy compliance summary
topics: [security, iac, audit, checkov, tfsec, trivy, tflint, compliance]
routing_hints: [checkov-scan, iac-audit, terraform-security, tfsec, trivy-config, misconfiguration-audit]
---

# IaC security audit

## When to use

Conducting automated security, compliance, and misconfiguration audits against Infrastructure-as-Code files (Terraform, OpenTofu, CloudFormation, Kubernetes YAML). Use when evaluating IaC repositories against CIS Benchmarks, NIST SP 800-53, or cloud provider best practices using Checkov, tfsec, Trivy, and TFLint.

## When not to use

Validating HCL syntax and generating plan files (`terraform-plan-validate`). Authoring or refactoring module definitions (`terraform-module-builder`). Mutating files or resolving findings in code without explicit triage.

## Criticality

High: provides preventive security guardrails and enforces encryption, least-privilege IAM, and network isolation standards prior to infrastructure deployment.

## Source of truth

- ai-router-only sources: `supporting/terraform/security-hardening.md`, `supporting/terraform/state-management.md`, `docs/standards/secure-configuration.md`, and `docs/standards/cloud-essentials.md`
- Standalone repositories should follow their local security/configuration rules and current official provider documentation.

## Isolation

Standalone dispatch: Follow the destination's isolation and dispatch rules. Use a registered local operator or continue in-session when those rules permit; report a capability gap if no local path supports the work.

`read-only`. In ai-router, the parent spawns `as-code-agent` with area `results`. Executes static analysis scans in read-only mode and writes structured findings reports without altering target manifests.

## How to use

1. Confirm target directory, frameworks (e.g. CIS AWS Foundation, NIST), and severity threshold from parent task.
2. Run Checkov static analysis scan:
   ```bash
   checkov -d <target_dir> --framework terraform -o json > checkov-results.json
   ```
3. Run TFLint provider ruleset validation:
   ```bash
   tflint --chdir=<target_dir> --format=json > tflint-results.json
   ```
4. If Trivy / tfsec is available on PATH, execute auxiliary AST scan:
   ```bash
   trivy config <target_dir> --format json -o trivy-results.json
   ```
5. Extract and aggregate violations:
   - Identify High and Critical severity findings (e.g. unencrypted S3 buckets, open security groups 0.0.0.0/0, missing KMS CMK rotation, wildcard IAM policies).
   - Audit suppression comments (`# checkov:skip=...`) to ensure valid justifications.
6. Compile comprehensive audit report under `results/as-code/audit/<topic>/<YYYY-MM-DD>/` containing summary table, resource breakdown, and specific HCL remediation snippets.

## Dry run

Execute checkov with `--soft-fail` or `--compact` to review findings without non-zero error termination:
```bash
checkov -d <target_dir> --framework terraform --compact --soft-fail
```

## Security

Inherits Critical cost layers in ai-router (qmd discovery; ast-grep for structured files; Headroom for bulky dumps). Standalone repositories follow their destination root `AGENTS.md` and tooling requirements.

A2A MUST NOT apply or deploy changes to real clouds. Never output plaintext credentials or exposed secrets found in scanned files. Sanitize audit output artifacts to prevent secret leakage.

## Completion gates

Completed security audit report detailing scan coverage, policy violations categorized by severity, compliant resources, and specific remediation instructions. Zero mutation of source files or remote state.
