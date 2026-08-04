---
name: insight-os-sales-coaching
description: >-
  Build evidence-backed coaching priorities with Insight OS MCP. Use whenever a Sale Manager
  asks who needs coaching, why performance changed, which objections are rising, who handles a
  topic well or poorly, or wants a 1:1 plan with real call examples, even without saying "MCP".
  Also use for Vietnamese requests such as "đội yếu ở đâu", "ai cần coach", "1:1 hôm nay",
  "đào tạo gì", or "tình trạng team". Use conversion-research for Marketing messaging.
---

# Insight OS — Sales Coaching

Use performance metrics to screen candidates, then require structured analysis and scoped call
evidence before making a coaching claim. This skill owns objections, handling, reactions, and
soft-close behavior.

## Interpret time language correctly

| User wording | Meaning | Do not assume |
|---|---|---|
| `1:1 hôm nay` | Meet today; plan the next 1–3 days | Diagnose from calendar today only |
| `1:1 tuần này` | Meet this week; plan the next 7–14 days | Diagnose from seven days only |
| `tháng này`, `Q2`, explicit range | Analysis window | — |

When only meeting timing is given, choose a dense diagnosis window such as 30–90 days and label
it **kỳ dữ liệu chẩn đoán**. Prefer recent example calls for the meeting.

## Workflow

### Team scan — at most 12 MCP calls

1. Resolve one timezone-aware primary window and optional comparison window.
2. Screen the scoped team with `insight_os_list_sales_performance`.
   - Sort by the user's question: rejection for skill problems, purchase for outcome screening,
     coverage for evidence quality, or calls for workload.
   - Read rates with `distinct_contacts`, call volume, coverage, and caveats. Never rank from one
     metric alone.
3. Deep-dive no more than three candidates with `insight_os_get_salesperson_analysis`.
4. For objection-led analysis, use `insight_os_search_insights` with
   `insight_types=["objection"]`, measure with `insight_os_aggregate_insights`, and confirm the
   canonical cluster with `insight_os_get_insight`.
5. Use redacted evidence summaries to support team-level patterns. Recommend a small priority set,
   each with a metric signal, evidence, one practice behavior, and a follow-up measure.

### One person and example calls — at most 8 MCP calls

1. Resolve the scoped salesperson.
   - If the user supplied only a name, call `insight_os_search_entities` with
     `entity_types=["salesperson"]`.
   - If several accessible people match, show minimal disambiguators and ask the manager to
     choose; never guess.
   - Open the selected `sale_id` with `insight_os_get_salesperson_analysis`.
2. Find and confirm the relevant canonical insight cluster. Restrict
   `insight_types=["objection"]` only when the request is objection-led; use the topic's actual
   insight type for need discovery, product issues, or other coaching moments.
3. Call `insight_os_list_evidence` with that `cluster_id` and `sale_id`.
   - Add `handling_statuses`, `customer_reactions`, `order_outcomes`, and the shared window when
     they express the coaching moment the manager wants.
   - Use a small limit. The filters must narrow the result; they never broaden authorization.
4. Open at most two returned call references with `insight_os_get_call_analysis`.
   - Keep transcript and audio disabled by default.
   - Choose recent, distinct examples that make the behavior observable.
5. If the requested `sale_id` is unavailable or out of scope, report it as unavailable. Do not
   infer whether that salesperson exists elsewhere.

Follow the public tool schema and pass business arguments at the top level.

## Metric fairness

- Unknown outcomes stay in the conversion denominator; `won` requires an order after the call.
- High-volume CTV/outbound roles can have structurally low purchase rates. Prefer rejection and
  unaddressed signals before calling this a selling-skill problem.
- Low insight coverage means thin evidence, not poor performance.
- One call is an example, not a recurring pattern. Use multiple calls when claiming recurrence.
- Metrics and call signals are associations, not proof of cause.

## Response

```text
# Coaching: [Tên] · 1:1 hôm nay|tuần này
Kỳ dữ liệu chẩn đoán: [from–to] · ví dụ cuộc: ưu tiên gần đây

## Kết luận nhanh — ai / việc gì / nghe call nào
## Bức tranh số
## Điểm mạnh
## Việc cần sửa (tối đa 2) + call reference + khoảnh khắc paraphrase
## Kế hoạch sau buổi
## Giới hạn dữ liệu
```

Keep facts and recommendations separate. In-scope salesperson display name, `sale_id`, and
selected `call_id` references are allowed when useful for the manager. Do not include customer or
household names, phones, external identifiers, full transcripts, or audio URLs.
