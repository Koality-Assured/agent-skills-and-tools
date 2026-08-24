# Agent Skills & Tools (`agent-skills-and-tools`)

[![CI](https://github.com/Koality-Assured/agent-skills-and-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/Koality-Assured/agent-skills-and-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](pyproject.toml)
[![Schema: Draft 2020-12](https://img.shields.io/badge/Schema-Draft_2020--12-green.svg)](schemas/)

## Mission Statement

`agent-skills-and-tools` is the official open-source ecosystem repository of verified, reusable agent skills, standard tool schemas, and operational utilities for autonomous coding and orchestration agents.

Our mission is to standardize how software engineering agents discover, inspect, and execute domain skills and tool integrations across diverse runtime harnesses while enforcing strict sandboxing, schema guarantees, and security boundaries.

## Architecture Overview

```
agent-skills-and-tools/
├── .github/workflows/ci.yml    # Continuous integration & schema validation
├── schemas/                    # Formal JSON Schema specifications
│   ├── skill.schema.json       # Frontmatter and metadata schema for SKILL.md
│   └── tool.schema.json        # Tool function declaration and parameter schema
├── skills/                     # Reusable domain skills library
│   ├── git-worktree-manager/   # Git worktree lifecycle management skill
│   └── ast-fact-extractor/     # AST symbol & call graph extraction skill
├── tools/                      # Validation CLI and integration utilities
│   ├── __init__.py
│   └── validator.py            # CLI validator for skills and tool declarations
├── tests/                      # Automated test suite
│   ├── __init__.py
│   └── test_skills.py          # Unit tests verifying skills against schemas
├── pyproject.toml              # Python project and dependency configuration
├── .editorconfig               # Editor configuration
├── .gitignore                  # Git ignore rules
└── LICENSE                     # MIT License
```

## Directory Structure

| Path | Purpose |
| --- | --- |
| `skills/` | Curated, validated agent skills with `SKILL.md`, examples, and execution guidance. |
| `schemas/` | Standard JSON Schemas (Draft 2020-12) defining skill frontmatter and tool parameters. |
| `tools/` | Python CLI utilities for schema linting, syntax verification, and packaging. |
| `tests/` | Unit and regression test suite executed in CI across Python versions. |

## Installation & Setup

### Prerequisites
- Python >= 3.10
- Git

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Koality-Assured/agent-skills-and-tools.git
cd agent-skills-and-tools

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies in editable mode
pip install -e ".[dev]"
```

## Usage

### Validate Skills and Schemas

Run the built-in validator against all skills in the repository:

```bash
# Validate all skills in skills/ against schemas/skill.schema.json
python tools/validator.py --all

# Validate a specific skill directory
python tools/validator.py --skill skills/git-worktree-manager

# Validate a specific tool schema
python tools/validator.py --tool-schema schemas/tool.schema.json
```

### Running Tests

```bash
python -m unittest discover -s tests -v
```

## Authoring a New Skill

Each skill resides in its own subdirectory under `skills/<skill-name>/` and must contain a `SKILL.md` file adhering to `schemas/skill.schema.json`.

Example `SKILL.md`:

```markdown
---
name: my-new-skill
description: Comprehensive description of when and how the agent must activate this skill.
version: 1.0.0
tags: [git, automation]
author: Koality-Assured
---

# My New Skill

## When to Use
- Detailed trigger conditions for the agent.

## Workflow Instructions
1. Step-by-step deterministic procedures.
```

## Security Notice

All skills and tool declarations in this repository are designed with defense-in-depth:
- **Sandbox Boundary:** Tool implementations MUST execute inside sandboxed or worktree-isolated environments.
- **AST Safety:** Code modification tools MUST validate syntax trees prior to filesystem commit.
- **Secret Isolation:** Tools MUST NOT log, leak, or interpolate raw environment credentials into agent prompts.

To report security vulnerabilities, please email security@koality-assured.org or open a GitHub Security Advisory.

## Contribution Guidelines

1. Fork the repository and create a feature branch (`feature/my-skill-name`).
2. Add your skill under `skills/<skill-name>/` with a valid `SKILL.md`.
3. Run `python tools/validator.py --all` and ensure tests pass: `python -m unittest discover -s tests -v`.
4. Submit a Pull Request with a clear description of the skill's capabilities and test coverage.

## License

Distributed under the [MIT License](LICENSE). Copyright (c) 2026 Koality-Assured.
