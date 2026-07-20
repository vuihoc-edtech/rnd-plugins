---
name: insight-os-sales-coaching
description: Analyze scoped sales performance and build evidence-backed coaching priorities with the bundled Insight OS MCP server. Use whenever a Sale Manager asks who needs coaching, why performance changed, which objections are rising, who handles an objection well or poorly, or requests team/member coaching actions grounded in customer calls.
---

# Insight OS Sales Coaching

Use the bundled `insight-os` MCP server. Treat performance metrics as screening signals, then verify coaching conclusions with structured salesperson, insight, evidence, and call data.

## Workflow

1. Establish one timezone-aware primary window and comparison window. Reuse them throughout the analysis.
2. Screen the scoped team with `insight_os_list_sales_performance`.
   - Choose `sort` to match the question: `purchase`, `rejection`, `coverage`, or `calls`.
   - Compare rates together with `distinct_contacts`, call volume, coverage, and returned caveats. Do not rank people from one metric alone.
3. Open candidate members with `insight_os_get_salesperson_analysis` to inspect strengths, weaknesses, recurring issues, and data status.
4. For objection-led coaching:
   - Use `insight_os_search_insights` with `insight_types=["objection"]` to resolve natural-language topics.
   - Use `insight_os_aggregate_insights` for primary/comparison metrics and segment breakdowns.
   - While the server follow-up for facet comparison is pending, use aggregate `group_by=["signal_group"]` instead of trusting the `signal_group` facet.
   - Confirm selected clusters with `insight_os_get_insight`.
5. Gather evidence progressively:
   - Start with `insight_os_get_evidence_summary`.
   - Use `insight_os_list_evidence` only if person/call-level evidence is visible and needed.
   - Follow selected call references with `insight_os_get_call_analysis`, without transcript/audio by default.
6. Recommend a small coaching priority set, each tied to a metric signal and concrete evidence.

Follow the live tool schema exactly. If the public schema exposes a single `params` object, place all business arguments inside it.

## Analysis Rules

- Distinguish correlation from cause. Metrics and recurring issues justify investigation; call evidence supports the coaching explanation.
- Inspect more than one call before describing a recurring behavior when evidence is available.
- Do not compare people outside the authenticated team/center scope or infer hidden members.
- Search results are candidates, not truth. Check label/description and evidence because semantically nearby clusters can drift.
- Preserve cohort suppression. Never estimate a suppressed count.
- If coverage is limited to consultation calls, do not attribute performance to ads, viewed content, or other un-ingested touchpoints.

## Response Shape

- `Ưu tiên coaching`: member/topic, why now, and confidence.
- `Bằng chứng định lượng`: window, key metrics, comparison, and sample size.
- `Bằng chứng cuộc gọi`: call references or redacted evidence summaries allowed by the principal.
- `Hành động coaching`: one observable behavior to practice and one follow-up measure.
- `Giới hạn dữ liệu`: caveats, coverage, cohort suppression, and access restrictions.

Keep facts and recommendations visibly separate.
