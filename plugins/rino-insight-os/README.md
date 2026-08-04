# Insight OS

Plugin nội bộ để khai thác catalog MCP read-only của Insight OS bằng bốn workflow theo user job.

## Thiết kế

- Một MCP server duy nhất tại `https://insight-os-api.rinoedu.ai/mcp`.
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

## Commands (Claude Code)

Mỗi command là một entry point gọi tay cho đúng một skill. Command không chứa workflow —
nó delegate rồi để skill giữ capability chain, call budget và output contract.

| Command | Skill | Argument |
|---|---|---|
| `/insight-os:customer-context` | `insight-os-customer-context` | `<tên khách \| số điện thoại \| contact_id>` |
| `/insight-os:sales-coaching` | `insight-os-sales-coaching` | `[tên sale \| team] [khoảng thời gian]` |
| `/insight-os:market-intelligence` | `insight-os-market-intelligence` | `<chủ đề \| nhận định cần verify> [segment] [khoảng thời gian]` |
| `/insight-os:conversion-research` | `insight-os-conversion-research` | `[target vs reference outcome] [segment] [khoảng thời gian]` |

Command đặt `disable-model-invocation: true`, nên model không tự gọi chúng. Auto-trigger vẫn chỉ đi
qua `description` của skill — giữ một đường routing duy nhất để eval còn ý nghĩa.

`argument-hint` phải được quote. Giá trị bắt đầu bằng `[` sẽ bị YAML đọc thành flow sequence và
frontmatter bị drop toàn bộ (`claude plugin validate` báo lỗi này).

## Cài trên Claude Code

```bash
claude plugin marketplace add vhrnd/plugins      # hoặc /absolute/path/to/plugins khi dev
claude plugin install insight-os@vuihoc-rnd
```

Restart Claude Code, rồi `/mcp` → chọn `insight-os` → authenticate. Kiểm tra plugin đã nạp đủ
component:

```bash
claude plugin details insight-os
```

Kết quả mong đợi: `Skills (8)` và 1 MCP server `insight-os`. Claude Code nạp `commands/*.md` và
`skills/*/SKILL.md` vào **cùng một namespace**, nên `details` đếm gộp: 4 skill `insight-os-*` cộng 4
command `customer-context`, `sales-coaching`, `market-intelligence`, `conversion-research`.
Command tốn khoảng 170 tok always-on cho cả bốn.

Nếu repo hoặc `~/.claude.json` của bạn đã tự khai báo `insight-os` trong `mcpServers`, xoá entry đó
sau khi cài plugin — nếu không sẽ có hai kết nối tới cùng server, gấp đôi số tool và hai luồng OAuth
riêng biệt.

## Authentication

Plugin dùng OAuth của Insight OS. URL MCP và OAuth resource cùng canonicalize về:

```text
https://insight-os-api.rinoedu.ai/mcp
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
- Trên Claude Code, cùng lý do: restart session sau khi `claude plugin update insight-os`, rồi
  `claude plugin validate plugins/insight-os` và `claude plugin details insight-os`.
- Khi sửa `description` của skill, chạy lại routing eval ở `evals/routing-*` (xem `evals/README.md`)
  vì bốn skill dùng chung nhiều từ khoá nhu cầu/objection.
- Conversion workflow bình thường không quá 5 MCP calls và drill down tối đa 3 evidence summaries.
- Coaching một người dùng `list_evidence` với `sale_id` cùng handling/reaction/outcome filters, rồi mở tối đa 2 call analyses.
