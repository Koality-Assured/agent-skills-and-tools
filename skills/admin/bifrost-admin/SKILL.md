---
name: bifrost-admin
description: >-
  Maxim Bifrost AI gateway configuration, route mappings, virtual keys, spend caps,
  and provider governance administration. Use when configuring Bifrost provider routes,
  managing client virtual keys, auditing gateway configurations, or adjusting inference
  policies across Anthropic Claude, OpenAI, and Gemini backends.
owner_agent: bifrost-operator
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
  - Target provider, route, or virtual key action, spend limit parameters, and configuration specification
  outputs:
  - Validated config.json updates, virtual key records, or route audit summaries
topics: [bifrost, gateway, inference, admin, virtual-keys, routing]
routing_hints: [bifrost-admin, bifrost, virtual-keys, route-mapping, ai-gateway]
---

# Bifrost administration

## When to use

Auditing, configuring, or administrating Maxim Bifrost AI gateway configuration files (`config.json`), model route definitions, provider credentials, and client Virtual Keys. Use when setting up fallback routes, registering new model providers (OpenAI, Anthropic, Gemini), managing spend caps and rate limits, or auditing client access policies.

## When not to use

Managing operating system daemon or container lifecycles (`bifrost-service`). General client application coding. Hardcoding plaintext secrets into repository files.

## Criticality

High: governs the central inference gateway configuration and upstream credential bindings.

## Source of truth

- `supporting/bifrost/config.json` (`../../../../supporting/bifrost/config.json`)
- `supporting/bifrost/architecture-and-inference.md` (`../../../../supporting/bifrost/architecture-and-inference.md`)
- `python supporting/bifrost/bifrost_manager.py`

## Isolation

mutate. Mutating operations require worktree isolation via `spawn_worktree.py`.

## How to use

1. Inspect the existing declarative gateway configuration:
   `python supporting/bifrost/bifrost_manager.py config`
2. Formulate changes to provider routes, fallback models, or virtual keys.
3. Ensure all upstream provider secrets reference environment variables (e.g. `env.OPENAI_API_KEY`) and never plaintext keys.
4. Validate the JSON schema and syntax before committing or restarting the gateway service.

## Dry run

`python supporting/bifrost/bifrost_manager.py validate-config`

## Security

Inherits Critical cost layers (qmd, ast-grep, and Headroom). Skills cannot waive them.

Zero plaintext secret exposure: all provider keys in `config.json` MUST use `env.<ENV_VAR>` syntax.
Client authentication defaults to optional for local workstation use, but Virtual Keys MUST be validated if `client.enforce_auth_on_inference` is enabled.

## Completion gates

`python supporting/bifrost/bifrost_manager.py validate-config` passes with zero errors, and configuration changes conform to Bifrost Schema V2 standards.
