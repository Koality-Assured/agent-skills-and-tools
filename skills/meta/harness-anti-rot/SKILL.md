---
schema_version: "2.0.0"
name: harness-anti-rot
description: >-
  Audits the harness control plane, worktrees, branches, scripts, and model guidance for rot, obsolescence, dead code, and stale artifacts. Use when checking for obsolete worktrees, dead scripts, merged branches, retired model references, or harness hygiene drift. Do not use for single code reviews (code-review-report) or adversarial PR critiques alone (antagonistic-review).
owner_agent: harness-operator
rank: high
isolation: read-only
on_failure: continue_with_partial
prerequisites:
  - git
  - python
dependencies:
  required_skills: []
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    - Optional --json flag, --check flag, or target repository root
  outputs:
    - Categorized Rot Ledger (merged worktrees, dead branches, orphaned scripts, deprecated models)
    - Actionable remediation recommendations and commands
topics: [harness, anti-rot, hygiene, control-plane, dead-code, worktrees, maintenance]
routing_hints: [harness-anti-rot, audit-rot, rot-audit, dead-code, stale-worktrees, branch-pruning, harness-hygiene]
---

# Harness Anti-Rot

Deterministic control-plane audit engine that scans the repository for worktree accumulation, merged Git branches, orphaned scripts, deprecated model strings, and operational memory drift.

## When to use

- Regular maintenance passes to identify debris from completed tasks and merged pull requests.
- Auditing repository health before major releases, downstream synchronization, or structural refactoring.
- Detecting orphaned scripts in `scripts/` with zero callers, zero skill references, and zero test coverage.
- Locating stale task worktrees in `scratch/worktrees/` that were merged into `main` and are ready for safe archiving via `harness clean --pr <number> --apply`.
- Pruning local `codex/*` branches that have already been merged into `main`.

## When not to use

- Single code reviews of an application or feature (`code-review-report`).
- Independent adversarial review of design or PR intent (`antagonistic-review`).
- Immediate routine worktree creation and post-merge archiving (`isolate-work` / `harness clean`).
- Ordinary memory adjustment (`memory-adjust`).

## Criticality

High. Harness rot impairs operator responsiveness, increases cognitive load, clutters Git worktree tracking, and causes `hybrid_dispatch.py` to index dead or superseded capabilities.

## Source of truth

- Script: `python scripts/routing/audit_harness_rot.py`
- CLI Entrypoint: `python scripts/cli/harness.py rot`
- Root `AGENTS.md` and `docs/guidance/agent-skill-pairing-discipline.md`
- Worktree lifecycle: [`ai-tooling/skills/meta/isolate-work/SKILL.md`](../isolate-work/SKILL.md)

## Isolation

`read-only`. The auditor is strictly non-mutating by default. Remediations (such as archiving worktrees or modifying code) must be executed through human-in-the-loop confirmation or dedicated isolated worktrees.

## How to use

1. Run the non-mutating audit:
   ```bash
   python scripts/routing/audit_harness_rot.py
   # Or via harness CLI:
   python scripts/cli/harness.py rot
   ```
2. Inspect the **Categorized Rot Ledger**:
   - **Merged Worktrees**: For each entry with `[MERGED READY TO CLEAN]`, execute the recommended preview and apply command:
     ```bash
     python scripts/cli/harness.py clean --pr <number> --apply
     ```
   - **Merged Local Branches**: Safely prune dead local branches:
     ```bash
     python scripts/routing/audit_harness_rot.py --fix-branches
     ```
   - **Orphaned Scripts**: Review each candidate. If it is a necessary recovery tool or spoke asset, annotate it with `# rot: exempt <reason>` in its docstring. If it is genuinely dead or superseded, propose an isolated deprecation PR.
   - **Deprecated Models**: Update docs or prompt templates referencing retired model generations to match `ai-tooling/agents/model-tiers.md`.

3. To enforce in CI or preflight, use the `--check` flag (returns non-zero if actionable rot is detected):
   ```bash
   python scripts/routing/audit_harness_rot.py --check
   ```

## Dry run

`python scripts/routing/audit_harness_rot.py --dry-run` or running without `--fix-branches` performs a complete non-mutating dry run.

## Security

Inherits Critical cost layers: QMD for discovery; ast-grep for structured files; Headroom for bulky dumps. Skills cannot waive root `AGENTS.md`.

Never force-remove worktrees (`git worktree remove --force`) or delete unmerged branches without verification. Use `harness clean --pr <num> --apply` to preserve the common Git archive under `<common Git dir>/ai-router-worktree-archives/`.

## Completion gates

Return the Rot Ledger to the orchestrator. If remediations were applied, confirm that `audit_harness_rot.py --check` passes cleanly.

> **Note:** This skill requires companion tooling not included in this catalog.
