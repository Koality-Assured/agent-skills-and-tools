---
name: confluence-doc-manage
description: >-
  Create, update, retrieve, search, and organize Confluence pages, spaces, and documentation trees across workspaces using REST API v2 and CQL. Use when publishing markdown or ADF documents to Confluence, querying page hierarchies, searching content with CQL, or updating existing documentation.
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
  - Target workspace (default koality-assured), space key or ID, page ID or title, body content (markdown/ADF/XHTML), CQL search query
  outputs:
  - Confluence page ID, URL, version number, and structured operation delivery report under results/
topics: [confluence, documentation, pages, spaces, cql, adf, publishing]
routing_hints: [confluence-doc-manage, create-confluence-page, update-confluence-page, search-cql, confluence-space, publish-docs]
---

# Confluence documentation and page management

Create, edit, organize, and search documentation pages and spaces in Confluence Cloud.

## When to use

- Publishing technical documentation, architectural designs, or release notes to Confluence.
- Creating and updating pages using Markdown, Atlassian Document Format (ADF), or XHTML storage format.
- Executing Confluence Query Language (CQL) searches to locate spaces, pages, blogposts, and attachments.
- Reading existing page content and inspecting ancestor hierarchies.
- Managing space homepages and parent-child page hierarchies.

## When not to use

- Auditing space permissions, group access, or global security settings (use `confluence-admin`).
- Authoring or packaging Atlassian Forge or Connect app descriptors (use `confluence-app-manage`).
- Processing or verifying inbound webhook events (use `confluence-webhook`).
- Sending chat notifications or Block Kit cards to Slack (use `slack-message`).

## Criticality

High. Outbound documentation published to organization-wide spaces represents authoritative institutional knowledge and must be accurately formatted and vetted.

## Source of truth

- CLI tool (single page): `scripts/confluence/confluence_ops.py`
- CLI tool (IA sync & drift): `scripts/confluence/confluence_sync.py`
- Oddities & drift test suite: `scripts/tests/test_confluence_oddities_and_drift.py`
- Interaction standard: [`docs/standards/confluence-interaction-and-administration.md`](../../../../docs/standards/confluence-interaction-and-administration.md)
- Synchronization & drift guide: [`docs/guidance/confluence-corpus-synchronization-and-drift.md`](../../../../docs/guidance/confluence-corpus-synchronization-and-drift.md)
- Architecture patterns: [`supporting/confluence/confluence-patterns.md`](../../../../supporting/confluence/confluence-patterns.md)
- ADF & Storage format guide: [`supporting/confluence/adf-and-storage-guide.md`](../../../../supporting/confluence/adf-and-storage-guide.md)

## Isolation

Mutating page operations must be tested via `--dry-run` first. Modifying space homepages, moving page hierarchies, or performing bulk page updates MUST run in the worktree the parent spawned.

## How to use

1. Discover Confluence formatting guidelines via `qmd search "confluence adf storage format"`.
2. Publish managed Wiki documentation to Confluence Information Security IA tree:
   ```bash
   python scripts/confluence/confluence_sync.py publish \
     --workspace koality-assured \
     --space-key "SEC" \
     --dry-run
   ```
3. Check for remote Confluence cloud edits (drift detection):
   ```bash
   python scripts/confluence/confluence_sync.py check-drift \
     --workspace koality-assured \
     --space-key "SEC"
   ```
4. Reconcile remote edits back into the local Wiki source:
   ```bash
   python scripts/confluence/confluence_sync.py pull-drift \
     --page-id "10844907" \
     --apply
   ```
5. Create a single new page from Markdown text in the `koality-assured` workspace:
   ```bash
   python scripts/confluence/confluence_ops.py create-page \
     --workspace koality-assured \
     --space-key "ENG" \
     --title "Architecture Overview" \
     --body "# System Architecture\n\nOverview of microservices." \
     --json
   ```
6. Update an existing page with new content and increment version:
   ```bash
   python scripts/confluence/confluence_ops.py update-page \
     --workspace koality-assured \
     --page-id "12345678" \
     --title "Architecture Overview v2" \
     --body "Updated architecture overview." \
     --version 2 \
     --json
   ```
7. Search pages using Confluence Query Language (CQL):
   ```bash
   python scripts/confluence/confluence_ops.py search-cql \
     --workspace koality-assured \
     --cql "space = 'ENG' and type = 'page' and text ~ 'architecture'" \
     --limit 10 \
     --json
   ```
8. Read page content:
   ```bash
   python scripts/confluence/confluence_ops.py get-page \
     --workspace koality-assured \
     --page-id "12345678" \
     --json
   ```

## Dry run

Preview page payload generation and simulated creation without network transmission:
```bash
python scripts/confluence/confluence_ops.py create-page \
  --workspace koality-assured \
  --space-key "ENG" \
  --title "Draft Specification" \
  --body "Preview text" \
  --dry-run \
  --json
```

## Security

Inherits Critical cost layers (qmd discovery, ast-grep for structured files, and Headroom for context compression). Skills cannot waive them.

Do not load general README.md for operations — hop area AGENTS.md, routing/skills, and qmd on kebab-case topic pages. README is human-only.

Never commit or log Confluence API tokens or email credentials. Always load from `CONFLUENCE_API_TOKEN` and `CONFLUENCE_EMAIL` environment variables.

Redact any sensitive credentials or internal keys before generating or updating documentation pages.

## Completion gates

- Page payload successfully constructed with valid ADF / Storage XHTML syntax.
- API response (or simulated dry-run confirmation) validated with page ID and status.
- No unredacted tokens or internal secrets in output logs or published content.
