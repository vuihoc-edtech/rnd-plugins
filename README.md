# Vuihoc R&D — AI Agent Plugin Marketplace

Marketplace plugin cho các AI Agent (**Claude Code** và **Codex**), do **Team R&D Vuihoc** cung cấp.

Repo này là nơi tập trung plugin nội bộ: kết nối MCP, skill workflow, và metadata marketplace để team cài một lần và dùng chung.

Hỗ trợ song song hai hệ sinh thái qua manifest riêng, **dùng chung cùng bộ `skills/` và cùng MCP endpoint**:

- **Claude Code** — `.claude-plugin/marketplace.json` (root) + `.claude-plugin/plugin.json` + `.claude-plugin/mcp.json` mỗi plugin.
- **Codex** — `.agents/plugins/marketplace.json` (root) + `.codex-plugin/plugin.json` + `.mcp.json` mỗi plugin.

## Plugins

| Plugin | Mô tả | MCP |
|--------|--------|-----|
| [`lms-review`](./plugins/lms-review) | Review dữ liệu LMS revise/practice qua MCP VUIHOC | `https://dev-mcp.vuihoc.vn/lms` |
| [`mark-flow`](./plugins/mark-flow) | Đọc/tìm script, daily script, catalog, comment, timeline MarkFlow Hub | `https://markflow-api.vuihoc.vn/mcp` |
| [`insight-os`](./plugins/insight-os) | Customer context, sales coaching, market và conversion intelligence có evidence | `https://insight-os-api.vuihoc.vn/mcp` |

## Cấu trúc repo

```text
.
├── .claude-plugin/marketplace.json    # metadata marketplace (Claude Code)
├── .agents/plugins/marketplace.json   # metadata marketplace (Codex)
├── plugins/
│   ├── lms-review/                    # plugin LMS Review
│   │   ├── .claude-plugin/            #   plugin.json + mcp.json (Claude Code)
│   │   ├── .codex-plugin/plugin.json  #   manifest (Codex)
│   │   ├── .mcp.json                  #   MCP config (Codex)
│   │   └── skills/                    #   dùng chung cả hai
│   ├── mark-flow/                     # plugin MarkFlow
│   │   ├── .claude-plugin/            #   plugin.json + mcp.json (Claude Code)
│   │   ├── .codex-plugin/plugin.json
│   │   ├── .mcp.json
│   │   ├── assets/
│   │   └── skills/
│   └── insight-os/                    # plugin Insight OS
│       ├── .claude-plugin/            #   plugin.json + mcp.json (Claude Code)
│       ├── .codex-plugin/plugin.json
│       ├── .mcp.json
│       └── skills/
└── README.md
```

## Yêu cầu

- **Claude Code** (≥ 2.1) hoặc **Codex CLI** (hoặc client tương thích plugin marketplace)
- Quyền truy cập MCP tương ứng (token VUIHOC cho `lms-review`, OAuth cho `mark-flow` và `insight-os`)

## Cài trên Claude Code

Thêm marketplace từ GitHub rồi cài plugin:

```bash
# trong Claude Code (slash command)
/plugin marketplace add vhrnd/plugins
/plugin install insight-os@vuihoc-rnd
/plugin install mark-flow@vuihoc-rnd
/plugin install lms-review@vuihoc-rnd
```

`@vuihoc-rnd` là `name` của marketplace (trong `.claude-plugin/marketplace.json`). Sau khi
install → skill trong plugin tự nạp, MCP server tự khởi động khi plugin được enable. Với
`insight-os`/`mark-flow`, Claude sẽ trigger OAuth khi gọi tool lần đầu.

`lms-review` cần token VUIHOC qua biến môi trường **`VUIHOC_TOKEN`** (được `mcp.json` tham chiếu
`${VUIHOC_TOKEN}`) — export trước khi mở Claude Code:

```bash
export VUIHOC_TOKEN="<token-cua-ban>"
```

Cài local (dev): `/plugin marketplace add /absolute/path/to/plugins`.
Kiểm tra manifest trước khi push: `claude plugin validate .` và `claude plugin validate plugins/<name>`.

## Cài trên Codex

Thêm marketplace từ GitHub:

```bash
codex plugin marketplace add https://github.com/vhrnd/plugins.git
```

Restart Codex → mở `/plugins` → chọn plugin cần dùng → Install → Enable.

### Cài local (dev)

```bash
codex plugin marketplace add /absolute/path/to/plugins
```

`lms-review` (Codex) cần header `token` VUIHOC trong `plugins/lms-review/.mcp.json`
(thay `<YOUR_VUIHOC_TOKEN>`).

## Plugin chi tiết

### LMS Review (`lms-review`)

- Kết nối MCP LMS để audit revise/practice
- Cần header `token` VUIHOC trong `plugins/lms-review/.mcp.json` (thay `<YOUR_VUIHOC_TOKEN>`)
- Skill kèm theo: `skills/lms-review`

### MarkFlow (`mark-flow`)

- Read-only MCP tới MarkFlow Hub
- Tool cho phép: search/get script & daily script, comments, catalog (class/subject/team/audience), timeline
- Auth: Codex trigger OAuth/login khi MCP yêu cầu
- Skill kèm theo: `skills/mark-flow`

### Insight OS (`insight-os`)

- Read-only capability catalog cho knowledge, evidence, entity/call và sales performance
- OAuth/row scope/redaction/cohort privacy do Insight OS enforce ở mỗi tool call
- Skills kèm theo: customer context, sales coaching, market intelligence và conversion research
- Skill luôn giữ evidence/caveat và không suy diễn touchpoint chưa được ingest

Có thể đổi URL MCP trong `plugins/mark-flow/.mcp.json` nếu dùng endpoint khác production.

## Thêm plugin mới

1. Tạo thư mục `plugins/<plugin-name>/` với:
   - `skills/<skill-name>/SKILL.md` (dùng chung cho cả Claude Code và Codex)
   - **Claude Code**: `.claude-plugin/plugin.json` (+ `.claude-plugin/mcp.json` nếu cần MCP;
     trỏ `"mcpServers": "./.claude-plugin/mcp.json"` trong `plugin.json`).
     MCP file dùng **bare map** `{"<server>": {"type": "http", "url": "..."}}` — không bọc key `mcpServers`.
   - **Codex**: `.codex-plugin/plugin.json` (+ `.mcp.json` nếu cần MCP).
2. Đăng ký entry ở **cả hai** manifest root: `.claude-plugin/marketplace.json` và
   `.agents/plugins/marketplace.json`.
3. `claude plugin validate .` để chắc chắn manifest Claude hợp lệ.
4. Cập nhật bảng Plugins trong README này.

> Lưu ý MCP: Claude Code đọc MCP từ `.claude-plugin/mcp.json` (qua tham chiếu trong `plugin.json`),
> còn Codex đọc từ `.mcp.json`. Giữ hai file riêng để mỗi hệ dùng đúng schema của mình; đừng để
> Claude auto-discover `.mcp.json` của Codex (khác định dạng).

## Bảo trì

- Giữ plugin độc lập trong `plugins/<name>/`
- Không commit token/secret; dùng placeholder và auth runtime
- Version plugin qua field `version` trong `plugin.json`

## Liên hệ

Team R&D — Vuihoc
