# Insight OS skill evaluations

- Each skill owns `evals/evals.json` with behavioral prompts and verifiable expectations.
- `skill-routing-evals.json` checks routing between the four overlapping Insight OS jobs.
- When improving a skill, compare against the marketplace version being replaced, not a
  prompt-only baseline.
- Run behavioral evaluations from a fresh authenticated MCP session so `tools/list` reflects the
  deployed schema.
- Grade process as well as prose: tool selection, filter propagation, privacy, call budget, and
  evidence round-trip are the discriminating behaviors.

## Two harnesses, one intent

| Suite | Format | Runner |
|---|---|---|
| `skill-routing-evals.json`, `skills/*/evals/evals.json` | Codex JSON (`query`/`expected_skill`, `prompt`/`expectations`) | Codex |
| `routing-*/prompt.md` + `graders/*.md` | Claude eval cases (`schema_version` 1.1) | `claude plugin eval insight-os@vuihoc-rnd` |

Both describe the same routing contract. Keep them in sync when a skill description changes —
`prompt.md` bodies are drawn verbatim from `skill-routing-evals.json`.

## Claude routing suite

Five cases cover the boundaries where the four skill descriptions overlap, not all twenty Codex
queries. Each case pins the skill that must fire and the neighbour that must not:

| Case | Boundary under test |
|---|---|
| `routing-conversion-research` | `objection` + market framing must not become coaching |
| `routing-market-intelligence` | needs/pains with no outcome cohort must not become an outcome comparison |
| `routing-sales-coaching` | objection handling by named salespeople is coaching, not research |
| `routing-customer-context` | one customer before one call must not become a segment study |
| `routing-negative-engineering` | editing the MCP server must fire no analysis skill |

Cases grade routing only. `allowed_tools` is `[Skill]` and `max_turns` is 4, so the graders observe
the `Skill` invocation and stop before any MCP call — routing is verifiable without OAuth. To grade
behaviour end to end instead, grant the catalog explicitly:

```bash
claude plugin eval insight-os@vuihoc-rnd --tag routing
claude plugin eval insight-os@vuihoc-rnd --allow-tools 'mcp__plugin_insight-os_insight-os__*'
```

`claude plugin eval` is gated behind early access. Until it is enabled on an account, these cases
are authored but unexecuted — treat their pass status as unknown, not green.
