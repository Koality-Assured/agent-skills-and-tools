---
name: bifrost-service
description: >-
  Maxim Bifrost AI gateway service, daemon, and container lifecycle operations.
  Use when starting, stopping, restarting, inspecting health, or checking logs
  for the local Bifrost gateway server process or Docker container environment.
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
  - Service action (start, stop, restart, status, health), deployment mode (native binary or Docker container), port, and host options
  outputs:
  - Service status reports, process IDs, container IDs, or health verification outputs
topics: [bifrost, service, daemon, container, docker, gateway]
routing_hints: [bifrost-service, bifrost, docker-compose, daemon, healthcheck, local-gateway]
---

# Bifrost service operations

## When to use

Managing the runtime lifecycle of the Maxim Bifrost AI gateway server. Use when starting, stopping, restarting, or checking the health of the local native Bifrost binary (`bifrost-http.exe`) or Docker Compose container deployment, verifying socket bindings (127.0.0.1:8080), inspecting logs, or validating inference readiness.

## When not to use

Administrating route definitions, provider credentials, or virtual keys (`bifrost-admin`). Client application-level prompt engineering. Managing unrelated background services.

## Criticality

High: controls the availability and health of the local inference gateway.

## Source of truth

- `supporting/bifrost/docker-compose.yml` (`../../../../supporting/bifrost/docker-compose.yml`)
- `supporting/bifrost/architecture-and-inference.md` (`../../../../supporting/bifrost/architecture-and-inference.md`)
- `python supporting/bifrost/bifrost_manager.py`

## Isolation

mutate. Mutating operations require worktree isolation via `spawn_worktree.py`.

## How to use

1. Check current runtime status and health:
   `python supporting/bifrost/bifrost_manager.py status`
2. Start the Bifrost gateway (defaults to native local binary if Docker is unavailable):
   `python supporting/bifrost/bifrost_manager.py start`
3. If Docker is available and containerized deployment is requested:
   `docker compose -f supporting/bifrost/docker-compose.yml up -d`
4. Verify HTTP health endpoint:
   `python supporting/bifrost/bifrost_manager.py health`
5. Test inference flow via harness:
   `harness chat --provider bifrost --query "test connection"`

## Dry run

`python supporting/bifrost/bifrost_manager.py status`

## Security

Inherits Critical cost layers (qmd, ast-grep, and Headroom). Skills cannot waive them.

Service processes must bind to loopback addresses (`127.0.0.1` or `localhost`) by default to prevent unauthorized external network access to the gateway.
Process and container logs must not expose raw upstream API keys.

## Completion gates

`GET /health` returns `200 OK` (or `bifrost_manager.py health` reports healthy), and process/container PID is verified running.
