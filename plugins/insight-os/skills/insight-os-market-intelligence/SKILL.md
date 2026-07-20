---
name: insight-os-market-intelligence
description: Research and verify customer or market signals with the bundled Insight OS MCP server. Use whenever Marketing, Product, CS, or leadership asks about customer needs, objections, trends, segment or time-window comparisons, campaign/research briefs, market claims, prevalence, outcomes, or evidence behind an Insight OS finding.
---

# Insight OS Market Intelligence

Use the bundled `insight-os` MCP server to turn aggregate customer-call signals into evidence-linked findings. Begin at aggregate knowledge and disclose finer-grained evidence only when the authenticated principal is allowed to see it.

## Workflow

1. Translate the question into an explicit, timezone-aware primary window, optional comparison window, insight types, and segment dimensions.
2. Discover available data with `insight_os_list_facets` and get an initial briefing with `insight_os_get_overview`.
   - Use only populated facets returned by the server.
   - While the server follow-up for comparison-aware facets is pending, do not use the `signal_group` facet for trend claims.
3. Resolve natural-language topics with `insight_os_search_insights`.
   - Inspect several plausible results when semantic overlap is broad.
   - Confirm the chosen canonical cluster with `insight_os_get_insight`; do not accept rank alone as proof.
4. Measure with `insight_os_aggregate_insights`.
   - Use no more than two `group_by` dimensions.
   - For rising/persistent/declining comparisons, use `group_by=["signal_group"]` with the same primary/comparison window.
   - Compare prevalence and affected customers only where cohort policy returns them.
5. Verify with `insight_os_get_evidence_summary` after narrowing to the most relevant cluster or small set of clusters.
   - Prefer redacted summaries for market-level work.
   - Escalate to detailed evidence/calls only when the user needs it and the capabilities are visible to the principal.
6. Produce the requested research, campaign, product, CS, or leadership brief. Every material claim must point to a returned metric or evidence item and include caveats.

Follow the live tool schema exactly. If the public schema exposes a single `params` object, place all business arguments inside it.

## Interpretation Rules

- Treat `data_health`, `caveats`, `access`, window, and comparison semantics as part of the result, not metadata to omit.
- `insufficient_cohort` means the system intentionally withholds the count and evidence. State that; never estimate it.
- Search results are retrieval candidates. Verify label, description, cluster metrics, and representative evidence before making a claim.
- The current source coverage may be call-consult only. Do not infer ad channel, content exposure, campaign causality, product usage, or other touchpoints unless returned data explicitly supports them.
- Separate observed signals from proposed messages, hypotheses, or actions.

## Response Shape

- `Câu hỏi và phạm vi`: primary/comparison windows, filters, and segments.
- `Kết luận chính`: concise evidence-backed answer.
- `Số liệu`: prevalence, affected customers, trend, outcome, and comparison as available.
- `Evidence`: representative redacted evidence or scoped references.
- `Hàm ý`: clearly labeled interpretation and recommended next action.
- `Caveats`: data health, source coverage, cohort suppression, redaction, and access constraints.

When the user asks to verify a claim, end with `Supported`, `Partially supported`, `Not supported`, or `Insufficient data`, followed by the decisive evidence.
