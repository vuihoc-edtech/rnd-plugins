---
name: insight-os-customer-context
description: >-
  Prepare evidence-backed pre-call customer context from Insight OS MCP. Use whenever a Sale
  or Manager asks to find a customer by name or phone, prepare for a call, review the journey,
  inspect recent calls, summarize objections or buying signals, or ask what happened on a
  customer call, even without saying "MCP". Also use for Vietnamese requests such as "chuẩn bị
  gọi", "context khách", "cuộc gần nhất", or "hành trình khách".
---

# Insight OS — Customer Context

Use the authenticated `insight-os` MCP server as the source of truth. Return only records visible
to the current principal.

## Workflow

1. Resolve the customer with `insight_os_search_entities`.
   - Use the name, phone fragment, or business identifier supplied by the user.
   - Prefer `entity_types=["customer"]` unless the request also needs calls or salespeople.
   - If several accessible customers match, show only the minimum disambiguating fields and ask
     the user to choose. Never guess.
2. Open the chosen stable `contact_id` with `insight_os_get_customer_context`.
3. Find calls with `insight_os_list_calls`.
   - Reuse the user's timezone-aware window. If none was given, state the effective window
     returned by the tool.
   - Filter by `contact_id`; follow `next_cursor` only when more history is necessary.
4. Inspect the latest or selected call with `insight_os_get_call_analysis`.
   - Keep `include_transcript=false` and `include_audio=false` by default.
   - Request raw media only when the user explicitly asks and the capability permits it.
5. Build the brief from returned journey, needs, buying signals, objections, outcome, and
   classification facts. Mark suggested talking points as recommendations.

Follow the public tool schema and pass business arguments at the top level.

## Rules

- `not_found` may mean outside scope. Say the record is unavailable to the current principal;
  do not infer whether it exists.
- Do not invent IDs or broaden from one customer to unrelated team rows.
- Do not expose transcript, phone, audio URL, or direct identifiers beyond what the user asked
  for and the returned access metadata permits.
- Surface relevant `data_health`, `caveats`, redaction, and access limits.

## Response

- **Khách hàng** — only identity and learning context needed for this task.
- **Tình hình gần nhất** — latest eligible call time, outcome/classification, and short summary.
- **Nhu cầu / buying signals** — returned facts.
- **Objections / rủi ro** — returned facts.
- **Gợi ý cuộc tiếp** — clearly labeled recommendations grounded in those facts.
- **Giới hạn dữ liệu** — coverage, caveats, and access constraints.

Include stable `contact_id` or `call_id` references only when they help the user continue.
