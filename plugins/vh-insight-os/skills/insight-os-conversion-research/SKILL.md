---
name: insight-os-conversion-research
description: >-
  Research outcome-associated customer needs and pains with Insight OS MCP for Marketing and
  Growth. Use for outcome-cohort comparisons such as won vs no_order or won vs lost, why
  customers close, conversion signals, messaging angles, or A/B hypotheses from calls, even
  without saying "MCP". Also use for Vietnamese requests
  such as "khách chốt khác gì", "insight cuộc gọi win", "lý do chốt", or "góc thông điệp".
  Use sales-coaching instead when the question is about a salesperson's handling behavior.
---

# Insight OS — Conversion Research

Use `insight_os_compare_outcome_insights` as the optimized path for outcome-cohort research.
The capability reports observed associations, not causal close reasons.

## Governing rules

- There is no modeled `close_reason` or customer-motivation field. Describe co-occurrence and
  turn actions into hypotheses to test; never present an association as why a customer bought.
- For Marketing, default to `insight_types=["customer_need", "pain_point"]`. If the user
  explicitly asks about barriers or objections associated with conversion, use
  `insight_types=["objection"]` for that comparison while keeping handling advice in coaching.
- Current coverage may be call/consult only. Do not infer channel, content, campaign, or ad
  attribution.
- Keep the main brief in plain Vietnamese. Do not show tool logs or raw API enums.

## Workflow — normal path at most 5 MCP calls

1. Call `insight_os_list_facets` only when outcomes or segment values must be discovered.
2. Make one `insight_os_compare_outcome_insights` call.
   - Default target to `won` and reference to `no_order`; use another outcome only when the user
     supplied it or facets confirmed it.
   - Default insight types to customer needs and pain points; switch to objections only for an
     explicit barrier/objection request.
   - Prefer `prevalence_delta`; use `relative_lift` only when the user wants rare but skewed
     signals.
   - Use the user's timezone-aware window or state a dense default explicitly.
3. Read the primary and comparison period summaries independently.
   - Report `observable_customers`, `customers_with_insights`, coverage, and overlap exclusion.
   - Rank from the primary matrix. Do not invent a difference-in-differences conclusion.
   - Treat handling/reaction breakdowns as cohort-level context, not properties of each cluster.
4. Select two or three themes. The comparison item already contains canonical label and
   description; use `insight_os_get_insight` only if that description is insufficient and reduce
   other drill-down calls to remain within the budget.
5. For evidence, call `insight_os_get_evidence_summary` for at most three selected themes.
   - Pass the item's complete `evidence_query` unchanged as `outcome_query`, together with the
     matching `cluster_id`.
   - Do not copy individual filters out of the signed query or combine it with explicit window,
     outcome, segment, handling, or reaction filters.
   - A modified, expired, or scope-mismatched query must fail closed; never fall back to broader
     cluster evidence.

## Response

```text
# [Target cohort] vs [reference cohort] — [needs/pains or explicit objection topic] · [window]

## Tóm tắt 30 giây
## Cỡ mẫu và coverage
   - observable customers / customers with insights for both cohorts
   - overlap excluded and any suppression
## Chủ đề sâu (2–3)
   - Cụm đang nói gì
   - Mức lệch giữa hai nhóm, using the named denominator
   - Cách khách diễn đạt, redacted
   - Cách đọc cho Marketing, explicitly non-causal
## Góc thông điệp thử
   - hypothesis · why · test · rejection condition
## Lưu ý
   - association, source coverage, overlapping buckets, and unavailable semantics
```

Render prevalence differences in percentage points when appropriate, while preserving the exact
denominator semantics returned by the tool.
