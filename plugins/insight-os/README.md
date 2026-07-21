# Insight OS

Plugin nội bộ để khai thác catalog MCP read-only của Insight OS bằng bốn workflow theo user job.

## Thiết kế

- Một MCP server duy nhất tại `https://insight-os-api.vuihoc.vn/mcp`.
- Tool ontology theo capability với prefix `insight_os_`, không theo persona.
- Skill phía client tổ chức workflow cho Sale, Sale Manager, Marketing và lãnh đạo.
- Server kiểm tra lại authorization, row scope, granularity, redaction và cohort privacy ở mỗi invocation.
- Skill không coi tool visibility là security control và không suy diễn dữ liệu chưa được ingest.

## Skills

| Skill | Job chính | Capability chain |
|---|---|---|
| `insight-os-customer-context` | Chuẩn bị trước cuộc gọi, xem hành trình khách và call gần nhất | entity search → customer context → calls → call analysis |
| `insight-os-sales-coaching` | Chọn người/chủ đề cần coaching và lấy đúng call mẫu | performance → salesperson analysis → insight → filtered evidence → call analysis |
| `insight-os-market-intelligence` | So sánh segment/time window và kiểm chứng nhận định thị trường | facets/overview → search/aggregate → insight → evidence summary |
| `insight-os-conversion-research` | So sánh cohort outcome và tạo messaging hypothesis | facets khi cần → outcome comparison → signed evidence summary |

## Authentication

Plugin dùng OAuth của Insight OS. URL MCP và OAuth resource cùng canonicalize về:

```text
https://insight-os-api.vuihoc.vn/mcp
```

Quyền thực tế phụ thuộc principal đăng nhập:

- Marketing: aggregate và redacted evidence summary khi cohort đủ lớn.
- Sale: entity/call rows do chính Sale sở hữu.
- Sale Manager: team hoặc center scope.
- Admin: explicit all-rows scope.

Nếu một capability không hiện ra hoặc resource trả not found, coi đó là kết quả policy-scoped; không tìm cách suy đoán sự tồn tại của dữ liệu.

## Runtime guardrails

- Luôn dùng time window có timezone và giữ cùng một window khi so sánh nhiều tool.
- Đọc `data_health`, `caveats` và `access` trước khi diễn giải kết quả.
- Cohort dưới ngưỡng chỉ được báo `insufficient_cohort`; không suy ngược count hoặc evidence.
- Chỉ xin transcript/audio khi người dùng yêu cầu rõ và capability hiện tại cho phép raw-call access.
- Không gán insight cho ads channel, content hoặc message nếu output chỉ xác nhận nguồn call-consult.
- Dùng public tool schema hiện tại và truyền business arguments ở top level.

## Outcome comparison

- Dùng `insight_os_compare_outcome_insights` cho câu hỏi won/no_order hoặc so sánh outcome cohort; không tự ghép các aggregate bucket.
- Mỗi ranked item trả `evidence_query`. Khi drill down, truyền object này nguyên vẹn vào tham số `outcome_query` của `insight_os_get_evidence_summary` cùng `cluster_id` tương ứng.
- Không copy từng filter ra khỏi signed query, không fallback sang evidence toàn cluster khi query hết hạn hoặc fail closed.
- Primary và comparison là hai ma trận độc lập. Không tự suy diễn difference-in-differences hoặc nguyên nhân chốt đơn.
- Handling/reaction breakdown là của toàn cohort, không phải breakdown riêng của từng ranked cluster.

## Release verification

- Sau khi MCP hoặc plugin thay đổi schema, dùng một Codex task mới để tránh cache `tools/list` từ session cũ.
- Conversion workflow bình thường không quá 5 MCP calls và drill down tối đa 3 evidence summaries.
- Coaching một người dùng `list_evidence` với `sale_id` cùng handling/reaction/outcome filters, rồi mở tối đa 2 call analyses.
