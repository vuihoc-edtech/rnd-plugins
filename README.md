# Vuihoc R&D — AI Agent Plugin Marketplace

Marketplace plugin cho các AI Agent (**Claude Code** và **Codex**), do **Team R&D Vuihoc** cung cấp.

Repo này là nơi tập trung plugin nội bộ: kết nối MCP, skill workflow, và metadata marketplace để team cài một lần và dùng chung.

Hỗ trợ song song hai hệ sinh thái qua manifest riêng, **dùng chung cùng bộ `skills/` và cùng MCP endpoint**:

- **Claude Code** — `.claude-plugin/marketplace.json` (root) + `.claude-plugin/plugin.json` mỗi plugin,
  MCP khai báo **inline** trong `plugin.json`.
- **Codex** — `.agents/plugins/marketplace.json` (root) + `.codex-plugin/plugin.json` + `.mcp.json` mỗi plugin.

> **Không tạo `.claude-plugin/mcp.json`.** Trước đây repo dùng file riêng này cho Claude và `.mcp.json`
> cho Codex. Claude Code CLI chấp nhận, nhưng **sync của claude.ai/Claude Desktop thì fail**: validator
> phía server đọc cả hai file, thấy cùng một tên MCP server với nội dung khác nhau và từ chối toàn bộ
> marketplace. Xem [Khai báo MCP](#khai-báo-mcp).

## Plugins

| Plugin | Mô tả | MCP | Phát hành |
|--------|--------|-----|-----------|
| [`insight-os`](./plugins/insight-os) | Customer context, sales coaching, market và conversion intelligence có evidence | `https://insight-os-api.vuihoc.vn/mcp` | Claude Code + Codex |
| [`mark-flow`](./plugins/mark-flow) | Đọc/tìm script, daily script, catalog, comment, timeline MarkFlow Hub | `https://markflow-api.vuihoc.vn/mcp` | Claude Code + Codex |
| [`vuihoc-content-authoring`](./plugins/vuihoc-content-authoring) | Giáo viên soạn câu hỏi LMS VUIHOC trong Claude, đăng nhập SSO VUIHOC | `https://docx-converter.vuihoc.vn/mcp` | **Claude only** (Claude Code, claude.ai) |
| [`lms-review`](./plugins/lms-review) | Review dữ liệu LMS revise/practice qua MCP VUIHOC | `https://dev-mcp.vuihoc.vn/lms` | **Codex only** |

`lms-review` không phát hành trên Claude Code — nó không có entry trong
`.claude-plugin/marketplace.json` nên `/plugin install lms-review@vuihoc-rnd` sẽ không tìm thấy.
Thư mục `plugins/lms-review/.claude-plugin/` được giữ lại để có thể bật lại sau; muốn phát hành lại
thì thêm entry vào manifest Claude. **Trước khi list lại**, phải chuyển MCP của nó sang inline và xoá
`plugins/lms-review/.claude-plugin/mcp.json` — plugin này vẫn còn cặp file gây collision và sẽ làm
sync claude.ai fail như trước. Xem [Khai báo MCP](#khai-báo-mcp).

## Cấu trúc repo

```text
.
├── .claude-plugin/marketplace.json    # metadata marketplace (Claude Code)
├── .agents/plugins/marketplace.json   # metadata marketplace (Codex)
├── plugins/
│   ├── lms-review/                    # plugin LMS Review — chỉ phát hành cho Codex
│   │   ├── .claude-plugin/            #   giữ lại nhưng KHÔNG listed ở marketplace Claude
│   │   ├── .codex-plugin/plugin.json  #   manifest (Codex)
│   │   ├── .mcp.json                  #   MCP config (Codex)
│   │   └── skills/
│   ├── mark-flow/                     # plugin MarkFlow
│   │   ├── .claude-plugin/plugin.json #   manifest + MCP inline (Claude Code)
│   │   ├── .codex-plugin/plugin.json
│   │   ├── .mcp.json                  #   MCP config (Codex)
│   │   ├── assets/
│   │   └── skills/
│   └── insight-os/                    # plugin Insight OS
│       ├── .claude-plugin/plugin.json #   manifest + MCP inline (Claude Code)
│       ├── .codex-plugin/plugin.json
│       ├── .mcp.json                  #   MCP config (Codex)
│       ├── commands/                  #   slash command (Claude Code)
│       ├── evals/                     #   routing eval: JSON (Codex) + case (Claude)
│       └── skills/                    #   dùng chung cả hai
└── README.md
```

## Yêu cầu

- **Claude Code** (≥ 2.1) hoặc **Codex CLI** (hoặc client tương thích plugin marketplace)
- Quyền truy cập MCP tương ứng (OAuth cho `mark-flow` và `insight-os`; token VUIHOC cho
  `lms-review`, chỉ dùng được qua Codex)

## Cài trên Claude Code

Thêm marketplace từ GitHub rồi cài plugin:

```bash
# trong Claude Code (slash command)
/plugin marketplace add vhrnd/plugins
/plugin install insight-os@vuihoc-rnd
/plugin install mark-flow@vuihoc-rnd
```

`@vuihoc-rnd` là `name` của marketplace (trong `.claude-plugin/marketplace.json`). Sau khi
install → skill trong plugin tự nạp, MCP server tự khởi động khi plugin được enable. Với
`insight-os`/`mark-flow`, Claude sẽ trigger OAuth khi gọi tool lần đầu.

Marketplace Claude chỉ phát hành hai plugin trên. `lms-review` là Codex only — xem mục
[Cài trên Codex](#cài-trên-codex).

Cài local (dev): `/plugin marketplace add /absolute/path/to/plugins`.
Kiểm tra manifest trước khi push: `claude plugin validate .` và `claude plugin validate plugins/<name>`.

> **Đừng để MCP bị nhân đôi.** Nếu trước đây bạn đã tự thêm cùng MCP server vào `mcpServers`
> (project scope trong `~/.claude.json`, hoặc `.mcp.json` của repo), hãy xoá entry đó sau khi cài
> plugin. Hai nguồn cùng khai báo một server sẽ tạo hai kết nối riêng (`mcp__<server>__*` và
> `mcp__plugin_<plugin>_<server>__*`) → gấp đôi số tool, hai luồng OAuth độc lập, và skill trở nên
> nhập nhằng khi nhắc tên tool. Kiểm tra bằng `claude plugin details <plugin>` và `/mcp`.

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

### LMS Review (`lms-review`) — Codex only

- **Không phát hành trên Claude Code.** Không có entry trong `.claude-plugin/marketplace.json`;
  chỉ cài được qua Codex.
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
- Slash command (Claude Code): `/insight-os:customer-context`, `/insight-os:sales-coaching`,
  `/insight-os:market-intelligence`, `/insight-os:conversion-research` — chỉ gọi tay, mỗi command
  delegate về skill tương ứng chứ không giữ workflow riêng
- Skill luôn giữ evidence/caveat và không suy diễn touchpoint chưa được ingest

Có thể đổi URL MCP trong `plugins/mark-flow/.mcp.json` nếu dùng endpoint khác production.

## Thêm plugin mới

1. Tạo thư mục `plugins/<plugin-name>/` với:
   - `skills/<skill-name>/SKILL.md` (dùng chung cho cả Claude Code và Codex)
   - **Claude Code**: `.claude-plugin/plugin.json`, khai báo MCP **inline** trong field `mcpServers`
     (object, không phải đường dẫn file). Xem [Khai báo MCP](#khai-báo-mcp).
   - **Codex**: `.codex-plugin/plugin.json` (+ `.mcp.json` nếu cần MCP).
2. Đăng ký entry ở manifest root của từng hệ muốn phát hành:
   `.claude-plugin/marketplace.json` (Claude Code) và/hoặc `.agents/plugins/marketplace.json` (Codex).
   Hai manifest độc lập, nên một plugin có thể chỉ phát hành cho một hệ — `lms-review` hiện chỉ có
   entry ở manifest Codex.
3. `claude plugin validate .` để chắc chắn manifest Claude hợp lệ.
4. Cập nhật bảng Plugins trong README này, kèm cột **Phát hành**.

## Khai báo MCP

Mỗi plugin khai báo MCP ở **đúng hai chỗ**, và Claude **không** được có file `mcp.json` riêng:

| Hệ | Nơi khai báo | Định dạng |
|---|---|---|
| Claude Code | field `mcpServers` **inline** trong `.claude-plugin/plugin.json` | object `{"<server>": {"type": "http", "url": "..."}}` |
| Codex | `.mcp.json` ở gốc plugin | theo schema Codex (bọc `mcpServers`, hoặc bare map) |

```json
// .claude-plugin/plugin.json
{
  "name": "my-plugin",
  "mcpServers": {
    "my-server": { "type": "http", "url": "https://example.vuihoc.vn/mcp" }
  }
}
```

Lý do không dùng `.claude-plugin/mcp.json`: validator của claude.ai/Claude Desktop đọc **cả**
`.mcp.json` **và** `.claude-plugin/mcp.json`. Nếu cùng một tên MCP server xuất hiện ở hai file với
nội dung khác nhau, sync fail và UI chỉ hiện thông báo chung *"Marketplace sync failed. Check the
repository URL and try again."* — không nói gì về MCP. Lỗi thật nằm ở
`~/Library/Logs/Claude/claude.ai-web.log`, tìm `MARKETPLACE_ERROR:REMOTE_SYNC_FAILED`:

```text
MCP server name 'insight-os' is declared with different content by both file '.mcp.json'
and file '.claude-plugin/mcp.json' — ... make the copies identical, remove one, or declare
the override inline in plugin.json
```

Repo này chọn cách thứ ba (inline) vì nó giữ file Codex nguyên vẹn và không thể drift trở lại.
`claude plugin validate --strict` **không** bắt được lỗi này — CLI dung thứ collision, chỉ server mới
từ chối. Sau khi sửa MCP, luôn thử `Add marketplace` lại trên Desktop rồi kiểm tra log.

## Bảo trì

- Giữ plugin độc lập trong `plugins/<name>/`
- Không commit token/secret; dùng placeholder và auth runtime
- Version plugin qua field `version` trong `plugin.json`

## Liên hệ

Team R&D — Vuihoc
