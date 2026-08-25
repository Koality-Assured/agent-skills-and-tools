---
name: public-llm-admin
description: >-
  Public AI vendor tenant, workspace, API key governance, and Zero Data Retention
  (ZDR) compliance administration and audits. Use when auditing public LLM
  workspaces, verifying data retention and privacy policies, managing spend caps,
  or rotating service keys across OpenAI, Anthropic, and Google AI platforms.
  Do not use for code-level prompt authoring or without human authorization for key changes.
owner_agent: public-llm-admin
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
topics: [llm, admin, ai-platforms, security, api-keys, zdr]
routing_hints: [public-llm-admin, openai, anthropic, gemini, api-keys, zdr, budgets]
---

# Public LLM administration

## When to use

Auditing, configuring, or governing public AI vendor workspaces, projects, API key lifecycles, and Zero Data Retention (ZDR) settings across Anthropic Claude, OpenAI / ChatGPT, and Google Gemini / Vertex AI. Use when verifying enterprise privacy compliance, reviewing active key inventories, checking monthly spend limits, or auditing key expiration policies.

## When not to use

Authoring application-level prompts or agent logic (`agent-builder`). Day-to-day code generation. Mutating API keys or workspace configurations without explicit human-turn authorization.

## Criticality

High: governs enterprise AI vendor privacy, compliance, and credential lifecycle.

## Source of truth

- [`docs/guidance/ai-platform-anthropic-claude.md`](../../../../docs/guidance/ai-platform-anthropic-claude.md)
- [`docs/guidance/ai-platform-openai-chatgpt.md`](../../../../docs/guidance/ai-platform-openai-chatgpt.md)
- [`docs/guidance/ai-platform-google-gemini.md`](../../../../docs/guidance/ai-platform-google-gemini.md)
- [`docs/standards/ai-development-security.md`](../../../../docs/standards/ai-development-security.md)
- `python scripts/llm/public_llm_admin.py`

## Isolation

`mutate`. Parent spawns `public-llm-admin` with area `results`. Key rotation and workspace configuration operations require explicit human authorization in the current turn.

## How to use

1. Confirm target provider (`anthropic`, `openai`, `gemini`) and workspace/project identifier.
2. For read-only compliance and workspace audit:
   ```bash
   python scripts/llm/public_llm_admin.py audit --provider <anthropic|openai|gemini> --workspace <identifier> --json
   ```
3. For checking spend caps and budget status:
   ```bash
   python scripts/llm/public_llm_admin.py spend --provider <anthropic|openai|gemini> --workspace <identifier> --json
   ```
4. For human-authorized key rotation or policy updates:
   - Verify explicit human confirmation.
   - Run dry-run to validate payload.
   - Execute mutation and record sanitized audit log under `results/llm/`.

## Dry run

```bash
python scripts/llm/public_llm_admin.py audit --provider openai --project proj-dev-sandbox --dry-run --json
python scripts/llm/public_llm_admin.py spend --provider anthropic --workspace ws-engineering-dev --dry-run --json
```

## Security

Inherits Critical cost layers (qmd discovery; ast-grep for structured files; Headroom for bulky dumps). Skills cannot waive them.

Never output, commit, or persist full API key values. Always redact keys to short metadata prefixes (e.g., `sk-proj-1234...`).

Key mutations require explicit authorization originating in the human's turn.

## Completion gates

Audit or rotation report recorded under `results/llm/`. Compliance flags (ZDR, spend caps) verified. No raw credentials logged.
