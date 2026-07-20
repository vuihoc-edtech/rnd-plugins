---
name: insight-os-customer-context
description: Prepare evidence-backed customer context from the bundled Insight OS MCP server. Use whenever a Sale or Manager asks to find a customer by name or phone, prepare for a call, review the customer journey, inspect recent calls, summarize objections or buying signals, or answer what happened in a specific customer call.
---

# Insight OS Customer Context

Use the bundled `insight-os` MCP server as the source of truth. Return only records visible to the authenticated principal.

## Workflow

1. Resolve the customer with `insight_os_search_entities`.
   - Search by the business identifier the user supplied.
   - Restrict `entity_types` to `customer` unless the request also needs calls or salespeople.
   - If several accessible customers match, present the minimal disambiguating fields and ask the user to choose. Do not guess.
2. Open the selected stable `contact_id` with `insight_os_get_customer_context`.
3. Determine the relevant call set with `insight_os_list_calls`.
   - Reuse the user's window. If none is given, state the effective window returned by the tool.
   - Filter by the selected `contact_id` and follow `next_cursor` only when more history is needed.
4. Inspect the latest or user-selected call with `insight_os_get_call_analysis`.
   - Keep `include_transcript=false` and `include_audio=false` by default.
   - Request raw transcript or audio only when the user explicitly needs it and the visible capability permits it.
5. Build the brief from returned facts: journey, buying signals, objections, latest call outcome/classification, and useful follow-up questions.

Follow the live tool schema exactly. If the public schema exposes a single `params` object, place all business arguments inside it.

## Safety and Evidence Rules

- A not-found result may mean outside-scope. Report that the record is unavailable to the current principal; do not reveal or infer whether it exists.
- Do not search by invented IDs or broaden from a customer to unrelated team data.
- Separate explicit call facts from suggested talking points.
- Never expose transcript, phone, audio URL, or direct identifiers beyond what the user requested and the returned access metadata permits.
- Preserve `data_health`, `caveats`, redaction, and access-granularity signals in the answer.

## Response Shape

Lead with a compact pre-call brief:

- `Khách hàng`: returned identity and learning segment needed for this task.
- `Tình hình gần nhất`: latest eligible call time, classification/outcome, and concise summary.
- `Nhu cầu / buying signals`: facts returned by Insight OS.
- `Objections / rủi ro`: facts returned by Insight OS.
- `Gợi ý cuộc gọi tiếp theo`: clearly marked recommendations grounded in the facts above.
- `Giới hạn dữ liệu`: caveats, missing coverage, or access restrictions.

Include stable contact/call references only when they help the user continue the investigation.
