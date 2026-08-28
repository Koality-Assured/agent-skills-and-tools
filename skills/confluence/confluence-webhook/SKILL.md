---
name: confluence-webhook
description: >-
  Configure, simulate, verify, and process Confluence Cloud and Atlassian Forge webhook events. Use when handling page or space lifecycle triggers, verifying HMAC-SHA256 signatures, validating webhook payloads, or integrating CI/CD event listeners.
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
  - Target workspace (default koality-assured), webhook payload JSON, headers (signature/timestamp/identifier), event type (page_created/page_updated/space_created)
  outputs:
  - Webhook verification status, parsed event summary, and processing output under results/
topics: [confluence, webhooks, events, hmac, security, automation]
routing_hints: [confluence-webhook, verify-confluence-webhook, simulate-confluence-event, page-created-event, doc-automation-trigger]
---

# Confluence webhook handling and event processing

Verify, simulate, and process Confluence webhook events for automated document synchronization and notifications.

## When to use

- Receiving and processing Confluence Cloud webhook events (`page_created`, `page_updated`, `page_trashed`, `space_created`).
- Verifying cryptographic signatures (HMAC-SHA256) on incoming Atlassian webhook requests.
- Simulating Confluence webhook payloads for local integration testing without triggering live external requests.
- Enforcing replay attack mitigation via timestamp freshness checks.
- Offloading synchronous webhook events to asynchronous background worker pipelines.

## When not to use

- Modifying or publishing Confluence page content directly (use `confluence-doc-manage`).
- Auditing space permissions or security access (use `confluence-admin`).
- Authoring Forge application manifests (use `confluence-app-manage`).
- Dispatching Slack notifications or incoming webhooks (use `slack-webhook` or `slack-message`).

## Criticality

High. Inbound webhooks process untrusted HTTP traffic and must strictly validate origin authenticity and protect against replay attacks.

## Source of truth

- CLI tool: `scripts/confluence/confluence_webhook.py`
- Webhook standard: [`docs/standards/confluence-app-development-and-webhooks.md`](../../../../docs/standards/confluence-app-development-and-webhooks.md)
- Architecture patterns: [`supporting/confluence/confluence-patterns.md`](../../../../supporting/confluence/confluence-patterns.md)
- Setup guide: [`docs/guidance/confluence-app-setup-and-webhooks.md`](../../../../docs/guidance/confluence-app-setup-and-webhooks.md)

## Isolation

Simulating webhook payloads or verifying signatures may run on primary. Modifying webhook subscription endpoints or mutating persistent handler configs runs in the worktree the parent spawned.

## How to use

1. Simulate an incoming `page_created` webhook event:
   ```bash
   python scripts/confluence/confluence_webhook.py simulate-event \
     --workspace koality-assured \
     --event-type page_created \
     --space-key "ENG" \
     --page-title "System Architecture" \
     --json
   ```
2. Verify an inbound webhook request signature:
   ```bash
   python scripts/confluence/confluence_webhook.py verify-signature \
     --signing-secret "$CONFLUENCE_SIGNING_SECRET" \
     --timestamp "1756298000" \
     --body '{"event":"page_created","page":{"id":"101"}}' \
     --signature "v0=abc123..." \
     --json
   ```
3. Parse and dispatch an event payload:
   ```bash
   python scripts/confluence/confluence_webhook.py handle-payload \
     --payload-file "event.json" \
     --json
   ```

## Dry run

Simulate webhook event reception and verification without external networking:
```bash
python scripts/confluence/confluence_webhook.py simulate-event \
  --workspace koality-assured \
  --event-type page_updated \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never store or expose webhook signing secrets or shared secrets.

Always enforce a 300-second maximum timestamp drift window to mitigate replay attacks.

## Completion gates

- Webhook signature cryptographically verified using constant-time comparison.
- Timestamp freshness confirmed within 300 seconds.
- Event payload parsed and validated against expected Confluence event schema.
