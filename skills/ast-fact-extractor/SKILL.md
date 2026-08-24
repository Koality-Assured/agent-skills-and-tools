---
name: ast-fact-extractor
description: Extract precise code facts, function signatures, class definitions, and call references using AST parsing to minimize LLM context cost.
version: 1.0.0
tags: [ast, compression, headroom, tier4, retrieval]
author: Koality-Assured
---

# AST Fact Extractor

## When to Use
- When an agent needs structural knowledge of a codebase without loading full file bodies into context.
- When implementing Tier-4 context headroom compression.
- When answering symbol reference queries or building architectural call graphs.

## Workflow Instructions

### 1. Symbol Extraction
- Parse target Python files using `ast.parse`.
- Extract class names, method signatures, docstrings, and decorator annotations.

### 2. Fact Emission
- Format extracted symbols as concise JSON or compact Markdown fact tables.
- Omit internal function bodies to conserve 85%+ token headroom.
