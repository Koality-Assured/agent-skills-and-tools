---
schema_version: "2.0.0"
name: benchlm-lookup
description: >-
  Queries, filters, and analyzes LLM performance benchmarks, context window limits,
  tokens-per-second speed, first-token latency, and token pricing ($/1M input, output, cached)
  from BenchLM (https://benchlm.ai/). Use when comparing model performance on coding,
  reasoning, agentic, multimodal, math, or cybersecurity benchmarks, evaluating price-to-performance
  ratios, selecting cost-efficient models for routing, or reviewing benchmark provenance.
  Do not use for general multi-topic research investigations (deep-research) or adversarial
  plan review (antagonistic-review).
owner_agent: detailed-activity
rank: high
isolation: read-only
on_failure: abort_and_rollback
prerequisites:
  - python
dependencies:
  required_skills: []
  delegated_skills: []
  in_session_skills: []
contracts:
  inputs:
    type: object
    properties:
      category:
        type: string
        enum: [overall, coding, reasoning, agentic, multimodal, math, cybersecurity]
      provider:
        type: string
      max_input_price:
        type: number
      max_output_price:
        type: number
      min_speed:
        type: number
      sort_by:
        type: string
        enum: [score, price_asc, price_desc, speed, value]
      limit:
        type: integer
  outputs:
    task_id: string
    status: string
    artifacts: list
    handoff_requests: list
    metrics: dict
---

# BenchLM lookup

## When to use

Comparing frontier and open-weight AI model performance, benchmark scores (SWE-bench, LiveCodeBench, HumanEval, GPQA Diamond, MMLU-Pro, ARC-AGI-2, OSWorld), token pricing ($ per 1M input/output/cached tokens), generation throughput (tokens/sec), and time-to-first-token latency. Use when the user asks to find the best performing model, the cheapest model meeting a quality floor, the highest price-to-performance model, or empirical benchmark evidence from [BenchLM.ai](https://benchlm.ai/).

## When not to use

Adversarial flaw ranking or design hole hunting (use `antagonistic-review`). Comprehensive multi-topic technology investigations (use `deep-research`). Dedicated prose anti-slop polishing without research context (use `anti-slop`).

## Criticality

High: Model selection, tiering, and routing decisions must be grounded in verified empirical benchmarks and transparent pricing data rather than subjective impressions.

## Source of truth

- [`https://benchlm.ai/`](https://benchlm.ai/)
- [`https://benchlm.ai/blog`](https://benchlm.ai/blog)
- [`references/valid-sources/ai-platforms-and-models.md`](../../../references/valid-sources/ai-platforms-and-models.md)
- [`scripts/research/benchlm_lookup.py`](../../../scripts/research/benchlm_lookup.py)
- [`docs/standards/research-and-empirical-validation.md`](../../../docs/standards/research-and-empirical-validation.md)

## Isolation

`read-only`. Does not mutate repository sources. Findings return to the orchestrator or write under `results/research/` when part of a broader dossier.

## How to use

1. Run benchmark and pricing lookup via the repo script:
   ```bash
   # Compare top models in coding by score
   python scripts/research/benchlm_lookup.py --category coding --sort score --limit 5

   # Find best price-to-performance models for agentic tasks
   python scripts/research/benchlm_lookup.py --category agentic --sort value --limit 5

   # Filter models under $1.00/1M input price with >60 tok/s speed
   python scripts/research/benchlm_lookup.py --max-input-price 1.00 --min-speed 60 --sort score
   ```
2. Emit structured results as JSON when required for programmatic downstream tooling:
   ```bash
   python scripts/research/benchlm_lookup.py --category reasoning --json
   ```
3. Synthesize findings into the response or report, quoting specific benchmark names and pricing metrics.

## Dry run

```bash
python scripts/research/benchlm_lookup.py --dry-run
python scripts/ai-tooling/validate_skill.py --skill benchlm-lookup --dry-run
```

## Security

Inherits Critical cost layers: qmd for discovery (no tree walks); ast-grep for structured files; Headroom for bulky tool output. Skills cannot waive root AGENTS.md.

Follow [`docs/agent-session-security.md`](../../../docs/agent-session-security.md). Treat remote benchmark metrics as external data; verify evidence tiers (`Supported` vs `Estimated`).

## Completion gates

Emit result envelope (`task_id`, `status`, `artifacts`, `metrics`). Append change history if tooling or references changed.
