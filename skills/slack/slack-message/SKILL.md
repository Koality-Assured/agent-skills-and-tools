---
name: slack-message
description: >-
  Compose, format, preview, and dispatch rich text and Block Kit messages to Slack channels, threads, and direct messages across workspaces. Use when sending Slack notifications, formatting Block Kit alert cards, querying channel message histories, or updating existing Slack messages.
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
  - Target workspace (default koality-assured), channel ID or name, message text or Block Kit JSON payload, thread timestamp
  outputs:
  - Message delivery confirmation, message timestamp (ts), structured delivery report under results/
topics: [slack, messaging, block-kit, notifications, collaboration]
routing_hints: [slack-message, send-slack, post-slack, block-kit-card, channel-alert, slack-notify]
---

# Slack message dispatch and Block Kit composition

Compose and dispatch structured Slack notifications, Block Kit cards, and channel thread replies.

## When to use

- Sending structured CI/CD notifications or operational alerts to Slack channels.
- Composing and rendering Block Kit UI cards with headers, field pairs, action buttons, and context footers.
- Posting replies into existing channel threads using message timestamps (`thread_ts`).
- Updating or deleting previously posted bot messages.
- Querying channel message histories for context extraction.

## When not to use

- Administering workspace security settings or SSO policies (use `slack-admin`).
- Sending one-off unauthenticated incoming webhooks without bot token access (use `slack-webhook`).
- Creating and configuring Slack App Manifests (use `slack-app-manage`).
- Sending emails or Google Workspace communications (use `google-gmail-manage`).

## Criticality

High. Outbound notifications are user-facing communications and must not contain unverified facts or credential leaks.

## Source of truth

- CLI tool: `scripts/slack/slack_ops.py`
- Interaction standard: [`docs/standards/slack-interaction-and-administration.md`](../../../../docs/standards/slack-interaction-and-administration.md)
- Block Kit guide: [`supporting/slack/block-kit-guide.md`](../../../../supporting/slack/block-kit-guide.md)
- Patterns: [`supporting/slack/slack-patterns.md`](../../../../supporting/slack/slack-patterns.md)

## Isolation

Mutating message dispatches must be tested via `--dry-run` first. Modifying workspace announcements or sending mass broadcast mentions (`@channel`, `@everyone`, `@here`) MUST halt unless explicitly authorized by the human in the current turn.

## How to use

1. Look up Slack message patterns via `qmd search "slack block kit ui composition"`.
2. Post a plain text notification:
   ```bash
   python scripts/slack/slack_ops.py post-message \
     --workspace koality-assured \
     --channel "general" \
     --text "Build pipeline finished successfully." \
     --json
   ```
3. Post a structured Block Kit notification card:
   ```bash
   python scripts/slack/slack_ops.py post-message \
     --workspace koality-assured \
     --channel "alerts-ci" \
     --text "Deployment Status: Success" \
     --header "🚀 Production Deployment" \
     --fields '{"Environment":"Production","Version":"v2.4.0","Status":"Clean"}' \
     --json
   ```
4. Query recent channel history:
   ```bash
   python scripts/slack/slack_ops.py list-messages \
     --workspace koality-assured \
     --channel "general" \
     --limit 10 \
     --json
   ```

## Dry run

Preview and validate message payloads without sending live network calls:
```bash
python scripts/slack/slack_ops.py post-message \
  --workspace koality-assured \
  --channel "general" \
  --text "Preview test message" \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never hardcode or commit Slack tokens (`xoxb-...`, `xoxp-...`). Always load from the `SLACK_BOT_TOKEN` environment variable.

Do not trigger broadcast mentions (`@channel`, `@everyone`, `@here`) without human confirmation.

## Completion gates

- Message payload successfully validated against Block Kit schema.
- Delivery confirmation (or simulated dry-run output) verified.
- No unredacted credentials or sensitive tokens emitted in output artifacts.
