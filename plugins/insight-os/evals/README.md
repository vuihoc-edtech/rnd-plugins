# Insight OS skill evaluations

- Each skill owns `evals/evals.json` with behavioral prompts and verifiable expectations.
- `skill-routing-evals.json` checks routing between the four overlapping Insight OS jobs.
- When improving a skill, compare against the marketplace version being replaced, not a
  prompt-only baseline.
- Run behavioral evaluations from a fresh authenticated MCP session so `tools/list` reflects the
  deployed schema.
- Grade process as well as prose: tool selection, filter propagation, privacy, call budget, and
  evidence round-trip are the discriminating behaviors.
