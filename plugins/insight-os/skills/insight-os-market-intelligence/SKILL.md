---
name: insight-os-market-intelligence
description: >-
  Research customer and market signals with Insight OS MCP. Use whenever Marketing, Product,
  CS, or leadership asks about needs, pains, segment portraits, trends, research briefs,
  prevalence, or verification of a market claim, even without saying "MCP". Also use for
  Vietnamese requests such as "chân dung segment", "phụ huynh lớp 9", "gần đây nổi gì",
  "xu hướng", or "verify nhận định". Use conversion-research instead for outcome-cohort
  comparisons such as won-vs-no_order or won-vs-lost.
---

# Insight OS — Market Intelligence

Start with aggregate knowledge, then use redacted evidence to explain what customers mean.
Lead with `customer_need` and `pain_point`. Treat `objection` as consultation-stage hesitation;
sales handling belongs in coaching. Outcome-cohort messaging belongs in
`insight-os-conversion-research`.

## Workflow

1. Resolve an explicit timezone-aware primary window and, for trend questions, a comparison
   window. Reuse them through the workflow.
2. Use `insight_os_list_facets` and `insight_os_get_overview` to learn which filters and source
   coverage are actually available.
3. For a natural-language topic, call `insight_os_search_insights`, inspect several plausible
   candidates, then confirm the selected canonical cluster with `insight_os_get_insight`.
   Search rank is retrieval, not proof; read label and description before interpreting it.
4. Measure with `insight_os_aggregate_insights`, using no more than two `group_by` dimensions.
   For trends, compare matching primary/comparison windows and read data health before using a
   signal group.
5. Verify two or three material themes with `insight_os_get_evidence_summary`. Prefer diverse,
   redacted representative items rather than near-duplicate examples.
6. Write the requested market, Product, CS, or leadership brief. Tie every material claim to a
   returned metric or evidence item.

Follow the public tool schema and pass business arguments at the top level.

## Interpretation

- Treat `data_health`, `caveats`, `access`, window, and comparison semantics as part of the
  result, not metadata to omit.
- `insufficient_cohort` means counts and evidence are intentionally withheld. Never estimate
  them.
- An empty comparison window or all-zero previous coverage means **dominant now**, not
  **verified rising**.
- Segment percentages use that segment's denominator. Insight buckets may overlap and do not
  need to sum to 100%.
- Current coverage may be call/consult only. Do not infer ad channel, content exposure,
  campaign effect, product usage, or causality unless returned data explicitly supports it.
- Separate observed signals from proposed messages, hypotheses, and actions.

## Response

- **Câu hỏi và phạm vi** — windows, filters, segment, and material coverage limits.
- **Kết luận chính** — a 30-second portrait a decision-maker can quote.
- **Họ muốn gì** — each theme: meaning, prevalence/base, and diverse redacted expressions.
- **Họ lo hoặc khó gì** — pain first; objections short and secondary where relevant.
- **Xu hướng** — only when comparison coverage supports one.
- **Hàm ý** — clearly labeled interpretation or recommendation.
- **Giới hạn dữ liệu** — health, source coverage, suppression, redaction, and access.

When verifying a claim, finish with **Supported**, **Partially supported**, **Not supported**, or
**Insufficient data**, followed by the decisive evidence.
