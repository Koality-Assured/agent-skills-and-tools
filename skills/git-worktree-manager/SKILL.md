---
name: git-worktree-manager
description: Manage dedicated git worktrees for isolated agent task execution, branch creation, and conflict-free concurrent editing.
version: 1.0.0
tags: [git, worktree, isolation, multi-agent]
author: Koality-Assured
---

# Git Worktree Manager

## When to Use
- When spawning subagents to work on independent feature branches without workspace collisions.
- When performing speculative refactoring that must remain isolated from the working tree.
- When running parallel test suites across different branches.

## Workflow Instructions

### 1. Worktree Creation
```bash
# Create dedicated branch and worktree
git worktree add scratch/worktrees/<branch-slug> -b agent/<YYYY-MM-DD>-<branch-slug>
```

### 2. Execution & Isolation
- All commands, edits, and test runs for the task MUST be confined to `scratch/worktrees/<branch-slug>`.
- Do not modify files in the root worktree or other sibling worktrees.

### 3. Cleanup & Teardown
```bash
# After branch is committed or merged
git worktree remove scratch/worktrees/<branch-slug>
git worktree prune
```
