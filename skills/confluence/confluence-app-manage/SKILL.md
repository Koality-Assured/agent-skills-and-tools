---
name: confluence-app-manage
description: >-
  Scaffold, validate, lint, and manage declarative Confluence Forge app manifests (manifest.yml) and Connect descriptors (atlassian-connect.json). Use when authoring Atlassian Forge apps, defining Confluence UI modules, configuring OAuth 2.0 scopes, or auditing app permissions for least privilege.
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
  - App name, description, app type (forge/connect), template (macro/spacePage/contextMenu/full), requested OAuth scopes
  outputs:
  - Validated manifest.yml or atlassian-connect.json file, lint report, and structure summary under results/
topics: [confluence, apps, forge, connect, manifest, oauth, modules]
routing_hints: [confluence-app-manage, forge-manifest, create-confluence-app, lint-forge-manifest, atlassian-connect]
---

# Confluence app management and Forge manifest authoring

Scaffold, validate, lint, and manage declarative Atlassian Forge and Connect app manifests.

## When to use

- Scaffolding a new Atlassian Forge app manifest (`manifest.yml`) for Confluence.
- Validating Forge module definitions (`confluence:spacePage`, `confluence:contextMenu`, `macro`, `contentAction`).
- Auditing and minimizing requested OAuth 2.0 scopes (`read:confluence-content.all`, `write:confluence-content`, `read:confluence-space.summary`).
- Validating legacy Atlassian Connect descriptors (`atlassian-connect.json`).
- Verifying manifest structure before deploying via the `forge deploy` CLI.

## When not to use

- Directly creating or updating page content in Confluence (use `confluence-doc-manage`).
- Auditing Confluence space permissions or global policies (use `confluence-admin`).
- Processing live webhook events from deployed apps (use `confluence-webhook`).
- Creating Slack App manifests (use `slack-app-manage`).

## Criticality

High. Application manifests dictate the security perimeters, data access permissions, and UI extension points within Atlassian Cloud.

## Source of truth

- CLI tool: `scripts/confluence/confluence_app_manifest.py`
- Development standard: [`docs/standards/confluence-app-development-and-webhooks.md`](../../../../docs/standards/confluence-app-development-and-webhooks.md)
- App patterns: [`supporting/confluence/confluence-app-patterns.md`](../../../../supporting/confluence/confluence-app-patterns.md)
- App setup guide: [`docs/guidance/confluence-app-setup-and-webhooks.md`](../../../../docs/guidance/confluence-app-setup-and-webhooks.md)

## Isolation

Scaffolding and editing manifest files must run in the worktree the parent spawned. Validating or linting existing manifest files may run on primary.

## How to use

1. Scaffold a new Forge app manifest for Confluence:
   ```bash
   python scripts/confluence/confluence_app_manifest.py generate \
     --template macro \
     --name "Document Metrics Macro" \
     --description "Renders real-time documentation health metrics on Confluence pages" \
     --output manifest.yaml
   ```
2. Validate and lint an existing Forge `manifest.yml`:
   ```bash
   python scripts/confluence/confluence_app_manifest.py validate \
     --file manifest.yaml \
     --json
   ```
3. Generate a complete multi-module Forge manifest:
   ```bash
   python scripts/confluence/confluence_app_manifest.py generate \
     --template full \
     --name "Koality Collaboration App" \
     --description "Full-featured collaboration app for Koality Assured" \
     --output manifest.yaml \
     --json
   ```

## Dry run

Validate manifest structures without writing files to disk:
```bash
python scripts/confluence/confluence_app_manifest.py validate \
  --file manifest.yaml \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Ensure all manifests strictly adhere to least privilege. Prohibit overly broad scopes when granular alternatives exist.

Never embed API tokens, client secrets, or sensitive environment variables in manifest files.

## Completion gates

- Manifest schema validated with zero structural errors.
- Requested OAuth scopes checked and minimized.
- Resulting manifest written cleanly to destination path.
