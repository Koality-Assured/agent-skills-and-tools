---
name: slack-app-manage
description: >-
  Generate, lint, validate, and convert declarative Slack App Manifests across YAML and JSON formats with least-privilege OAuth scope enforcement. Use when scaffolding new Slack apps, validating manifest schemas, converting manifests between formats, or configuring app features and event subscriptions.
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
  - App archetype template (webhook-notifier, slash-command-bot, full-bot), app metadata, input manifest path
  outputs:
  - Generated manifest file (YAML/JSON), validation error report, scope security assessment
topics: [slack, manifest, app, oauth, permissions, configuration]
routing_hints: [slack-app-manage, slack-manifest, app-manifest, generate-manifest, validate-manifest]
---

# Slack App Manifest management

Generate, validate, and manage declarative Slack App Manifests with least-privilege OAuth scopes.

## When to use

- Scaffolding new Slack App Manifests for common archetypes (alerting bots, slash commands, interactive tools).
- Validating an existing Slack App Manifest against the official Slack schema specification.
- Converting manifests between YAML and JSON formats.
- Auditing requested OAuth bot and user scopes for least privilege compliance.
- Configuring event subscriptions, slash commands, and Socket Mode settings.

## When not to use

- Sending messages to existing channels (use `slack-message`).
- Dispatching one-off webhook alerts (use `slack-webhook`).
- Auditing workspace-wide user permissions and SSO policies (use `slack-admin`).

## Criticality

High. App Manifests define the complete permission perimeter and security boundaries of custom Slack applications.

## Source of truth

- CLI tool: `scripts/slack/slack_app_manifest.py`
- App standard: [`docs/standards/slack-app-development-and-webhooks.md`](../../../../docs/standards/slack-app-development-and-webhooks.md)
- Manifest guide: [`supporting/slack/app-manifest-guide.md`](../../../../supporting/slack/app-manifest-guide.md)

## Isolation

Mutating manifest generation and editing runs in an isolated worktree. Validating and converting manifests is read-only.

## How to use

1. Generate an alerting bot manifest:
   ```bash
   python scripts/slack/slack_app_manifest.py generate \
     --template webhook-notifier \
     --name "Koality Alert Bot" \
     --output manifest.yaml
   ```
2. Generate a full interactive bot manifest:
   ```bash
   python scripts/slack/slack_app_manifest.py generate \
     --template full-bot \
     --name "Koality Assistant" \
     --output manifest.yaml
   ```
3. Validate a manifest file:
   ```bash
   python scripts/slack/slack_app_manifest.py validate \
     --file manifest.yaml \
     --json
   ```
4. Convert YAML manifest to JSON:
   ```bash
   python scripts/slack/slack_app_manifest.py convert \
     --input manifest.yaml \
     --output manifest.json
   ```

## Dry run

Validate manifest generation in-memory without writing to disk:
```bash
python scripts/slack/slack_app_manifest.py generate \
  --template webhook-notifier \
  --name "Test Bot" \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Ensure all manifests adhere to the principle of least privilege, avoiding deprecated or overprivileged scopes.

Do not store client secrets or app tokens inside manifest files.

## Completion gates

- Manifest passes schema validation with zero structural errors.
- Requested OAuth scopes conform to least privilege.
- Generated files stored under version control.
