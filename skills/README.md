# Skills

Human overview: router skills live here as `<name>/SKILL.md`.

**Agents do not use this README as a catalog.** They load [`../../routing/skill-dispatch.md`](../../routing/skill-dispatch.md) (regenerate with `python scripts/routing/generate_skill_dispatch.py`) and spawn `owner_agent`. Template: [`../../ai-tooling/skills/skill-conventions.md`](skill-conventions.md). Validate: `python scripts/ai-tooling/validate_skill.py --all`.

Human index (not agent SoT):

| Skill | Owner | Isolation |
| --- | --- | --- |
| [`agent-builder/`](./agent-builder/) | ai-tooling-ops | mutate |
| [`antagonistic-review/`](./antagonistic-review/) | detailed-activity | mutate |
| [`anti-slop/`](./anti-slop/) | artifact-agent | mutate |
| [`architecture-diagram/`](./architecture-diagram/) | artifact-agent | mutate |
| [`as-code-builder/`](./as-code-builder/) | as-code-agent | mutate |
| [`ast-grep/`](./ast-grep/) | router-maintenance | read-only |
| [`aws-logs/`](./aws-logs/) | cloud-operator | mutate |
| [`aws-read/`](./aws-read/) | cloud-operator | mutate |
| [`aws-write/`](./aws-write/) | cloud-operator | mutate |
| [`azure-logs/`](./azure-logs/) | cloud-operator | mutate |
| [`azure-read/`](./azure-read/) | cloud-operator | mutate |
| [`azure-write/`](./azure-write/) | cloud-operator | mutate |
| [`code-review-report/`](./code-review-report/) | artifact-agent | mutate |
| [`corpus-draft/`](./corpus-draft/) | artifact-agent | mutate |
| [`cost-layer-dry-run/`](./cost-layer-dry-run/) | router-maintenance | mutate |
| [`deep-research/`](./deep-research/) | detailed-activity | mutate |
| [`doc-builder/`](./doc-builder/) | documentation-ops | mutate |
| [`executive-report/`](./executive-report/) | artifact-agent | mutate |
| [`foundation-site/`](./foundation-site/) | artifact-agent | mutate |
| [`framework-mapper/`](./framework-mapper/) | artifact-agent | mutate |
| [`gcp-logs/`](./gcp-logs/) | cloud-operator | mutate |
| [`gcp-read/`](./gcp-read/) | cloud-operator | mutate |
| [`gcp-write/`](./gcp-write/) | cloud-operator | mutate |
| [`git-basics/`](./git-basics/) | git-fast-operator | mutate |
| [`github-paths/`](./github-paths/) | github-ops | read-only |
| [`github-workflow/`](./github-workflow/) | github-ops | mutate |
| [`guidance-draft/`](./guidance-draft/) | artifact-agent | mutate |
| [`headroom/`](./headroom/) | router-maintenance | read-only |
| [`humanizer/`](./humanizer/) | artifact-agent | mutate |
| [`isolate-work/`](./isolate-work/) | router-maintenance | mutate |
| [`markdownlint/`](./markdownlint/) | documentation-ops | mutate |
| [`memory-adjust/`](./memory-adjust/) | ai-tooling-ops | mutate |
| [`memory-cleanup/`](./memory-cleanup/) | ai-tooling-ops | mutate |
| [`memory-create/`](./memory-create/) | ai-tooling-ops | mutate |
| [`mermaid-diagram/`](./mermaid-diagram/) | artifact-agent | mutate |
| [`noir-scan/`](./noir-scan/) | artifact-agent | mutate |
| [`proposal-report/`](./proposal-report/) | artifact-agent | mutate |
| [`qmd-efficiency/`](./qmd-efficiency/) | qmd-ops | mutate |
| [`qmd-usage/`](./qmd-usage/) | qmd-ops | read-only |
| [`reference-maintain/`](./reference-maintain/) | reference-ops | mutate |
| [`scratch-cleanup/`](./scratch-cleanup/) | router-maintenance | mutate |
| [`script-builder/`](./script-builder/) | script-ops | mutate |
| [`skill-builder/`](./skill-builder/) | ai-tooling-ops | mutate |
| [`skill-dry-run/`](./skill-dry-run/) | ai-tooling-ops | read-only |
| [`sync-downstream-repos/`](./sync-downstream-repos/) | repo-sync-ops | mutate |
| [`tabler-dashboard/`](./tabler-dashboard/) | artifact-agent | mutate |
| [`threat-model/`](./threat-model/) | assessment-agent | mutate |
| [`wiki-structure/`](./wiki-structure/) | documentation-ops | read-only |
