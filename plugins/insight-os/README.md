# Insight OS

Plugin nội bộ để khai thác catalog MCP read-only của Insight OS bằng các workflow có chủ đích.

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
| `insight-os-sales-coaching` | Chọn người/chủ đề cần coaching và truy về call evidence | performance → salesperson analysis → insight/evidence → call analysis |
| `insight-os-market-intelligence` | So sánh segment/time window và kiểm chứng nhận định thị trường | facets/overview → search/aggregate → insight → evidence summary |

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
- Follow live tool schema. Nếu schema yêu cầu một object `params`, đặt toàn bộ business arguments trong object đó.

## Known production follow-up

Issue Insight OS #56 đang theo dõi correctness của `signal_group` facet, hybrid-search precision, evidence-summary latency và public `params` wrapper. Trong lúc issue còn mở:

- Dùng `insight_os_aggregate_insights(group_by=["signal_group"])` thay vì facet `signal_group` để so primary/comparison window.
- Xác minh semantic match bằng `insight_os_get_insight` và evidence trước khi chọn search result.
- Chỉ gọi evidence summary sau khi đã thu hẹp còn một vài cluster phù hợp.
