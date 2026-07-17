# Vuihoc R&D — AI Agent Plugin Marketplace

Marketplace plugin cho các AI Agent (Codex và tương thích), do **Team R&D Vuihoc** cung cấp.

Repo này là nơi tập trung plugin nội bộ: kết nối MCP, skill workflow, và metadata marketplace để team cài một lần và dùng chung.

## Plugins

| Plugin | Mô tả | MCP |
|--------|--------|-----|
| [`lms-review`](./plugins/lms-review) | Review dữ liệu LMS revise/practice qua MCP VUIHOC | `https://dev-mcp.vuihoc.vn/lms` |
| [`mark-flow`](./plugins/mark-flow) | Đọc/tìm script, daily script, catalog, comment, timeline MarkFlow Hub | `https://markflow-api.vuihoc.vn/mcp` |

## Cấu trúc repo

```text
.
├── .agents/plugins/marketplace.json   # metadata marketplace
├── plugins/
│   ├── lms-review/                    # plugin LMS Review
│   │   ├── .codex-plugin/plugin.json
│   │   ├── .mcp.json
│   │   └── skills/
│   └── mark-flow/                     # plugin MarkFlow
│       ├── .codex-plugin/plugin.json
│       ├── .mcp.json
│       ├── assets/
│       └── skills/
└── README.md
```

## Yêu cầu

- Codex CLI (hoặc client hỗ trợ Codex plugin marketplace)
- Quyền truy cập MCP tương ứng (token VUIHOC cho `lms-review`, OAuth/MarkFlow access cho `mark-flow`)

## Cài marketplace

Thêm marketplace từ GitHub:

```bash
codex plugin marketplace add https://github.com/vhrnd/plugins.git
```

Restart Codex → mở `/plugins` → chọn plugin cần dùng → Install → Enable.

### Cài local (dev)

```bash
codex plugin marketplace add /absolute/path/to/plugins
```

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

Có thể đổi URL MCP trong `plugins/mark-flow/.mcp.json` nếu dùng endpoint khác production.

## Thêm plugin mới

1. Tạo thư mục `plugins/<plugin-name>/` với:
   - `.codex-plugin/plugin.json`
   - `.mcp.json` (nếu cần MCP)
   - `skills/<skill-name>/SKILL.md` (nếu cần skill)
2. Đăng ký entry trong `.agents/plugins/marketplace.json`
3. Cập nhật bảng Plugins trong README này

## Bảo trì

- Giữ plugin độc lập trong `plugins/<name>/`
- Không commit token/secret; dùng placeholder và auth runtime
- Version plugin qua field `version` trong `plugin.json`

## Liên hệ

Team R&D — Vuihoc
