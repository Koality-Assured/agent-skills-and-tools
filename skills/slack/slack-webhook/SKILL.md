---
name: slack-webhook
description: >-
  Dispatch incoming Slack webhooks and verify inbound webhook request signatures using HMAC-SHA256 and timestamp replay protection. Use when sending alert webhooks to Slack, verifying incoming Events API or Slash Command HTTP requests, or building webhook endpoint handlers.
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
  - Webhook URL or HTTP request headers/body, raw payload, signing secret, verification timestamp
  outputs:
  - Webhook delivery confirmation, HMAC-SHA256 signature verification status, audit report
topics: [slack, webhook, security, hmac, signature-verification, events-api]
routing_hints: [slack-webhook, send-webhook, verify-slack-signature, incoming-webhook, events-api-verify]
---

# Slack webhook dispatch and HMAC signature verification

Dispatch incoming webhook alerts and cryptographically verify inbound Slack event payloads.

## When to use

- Sending lightweight notifications and CI/CD status cards via pre-configured Incoming Webhooks.
- Verifying inbound HTTP requests from Slack (Events API, Interactivity, Slash Commands) using HMAC-SHA256.
- Enforcing timestamp freshness (300-second window) to defend against replay attacks.
- Testing webhook payload construction in local development or CI/CD pipelines.

## When not to use

- Full bidirectional bot interactions with modals and channel reads (use `slack-message`).
- Administering workspace security settings (use `slack-admin`).
- Scaffolding and converting Slack App Manifests (use `slack-app-manage`).

## Criticality

High. Inbound webhooks must be authenticated to prevent remote unauthorized command execution and forged events.

## Source of truth

- CLI tool: `scripts/slack/slack_ops.py`
- App standard: [`docs/standards/slack-app-development-and-webhooks.md`](../../../../docs/standards/slack-app-development-and-webhooks.md)
- Patterns: [`supporting/slack/slack-patterns.md`](../../../../supporting/slack/slack-patterns.md)

## Isolation

Mutating webhook dispatches run in an isolated worktree or dry-run mode. Verification of cryptographic signatures is read-only.

## How to use

1. Dispatch an incoming webhook alert:
   ```bash
   python scripts/slack/slack_ops.py send-webhook \
     --webhook-url "https://hooks.slack.com/services/T00/B00/XXX" \
     --text "Alert: CPU usage exceeded 85%" \
     --header "⚠️ Infrastructure Alert" \
     --status-badge "warning" \
     --json
   ```
2. Verify inbound Slack request signature:
   ```bash
   python scripts/slack/slack_ops.py verify-signature \
     --signing-secret "$SLACK_SIGNING_SECRET" \
     --timestamp "1756300000" \
     --body '{"command":"/status"}' \
     --signature "v0=a1b2c3d4e5f6..." \
     --json
   ```

## Dry run

Test webhook payload formatting without network transmission:
```bash
python scripts/slack/slack_ops.py send-webhook \
  --webhook-url "https://hooks.slack.com/services/T00/B00/MOCK" \
  --text "Dry run webhook alert" \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Webhook URLs are bearer credentials. Never commit or log raw webhook URLs.

Always verify incoming requests using constant-time string comparison (`hmac.compare_digest`) and reject requests older than 300 seconds.

## Completion gates

- Webhook payload delivered (or simulated in dry-run mode).
- HMAC-SHA256 signatures validated with timing-attack resistance.
- Zero credentials or tokens committed to git.
