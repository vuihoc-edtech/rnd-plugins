# Vuihoc R&D — Multi-Agent Plugin Marketplace

Kho lưu trữ và phân phối tập trung các Plugin (kết nối **MCP Server** + bộ **Agent Skills** + **Slash Commands**) của **Team R&D VUIHOC**, tương thích với toàn bộ các trợ lý AI phổ biến hiện nay:

- **Claude** (`claude.ai`, Claude Desktop, Cowork, Claude Code) — `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`
- **OpenAI Codex & ChatGPT** (Codex CLI, ChatGPT Desktop Work Mode) — `.agents/plugins/marketplace.json` + `.codex-plugin/plugin.json` + `.mcp.json`
- **Cursor IDE** — `.cursor-plugin/marketplace.json` + `.cursor-plugin/plugin.json` + `.mcp.json`
- **Gemini CLI** — `gemini-extension.json` + `GEMINI.md`
- **Windsurf, VS Code Copilot, Cline, Roo Code, OpenCode & 70+ Agent khác** — qua chuẩn mở [Agent Skills (`npx skills`)](https://skills.sh)

---

## Danh sách Plugins

| Plugin | Phiên bản | Mô tả | MCP Endpoint | Nền tảng hỗ trợ |
|--------|-----------|-------|--------------|-----------------|
| [`vuihoc-content-authoring`](./plugins/vuihoc-content-authoring) | `1.0.0` | Giáo viên VUIHOC soạn, giải kiểm chứng và rà soát câu hỏi LMS qua MCP (đăng nhập VUIHOC SSO) | `https://docx-converter.vuihoc.vn/mcp` | **Đa nền tảng** (Claude, Codex/ChatGPT, Cursor, Gemini CLI, Windsurf, `npx skills`) |
| [`mark-flow`](./plugins/mark-flow) | `0.1.0` | Đọc/tìm script, daily script, catalog, comment, timeline MarkFlow Hub | `https://markflow-api.vuihoc.vn/mcp` | Claude + Codex + Cursor |
| [`vh-insight-os`](./plugins/vh-insight-os) (`insight-os`) | `0.2.0` | Customer context, sales coaching, market và conversion intelligence có evidence cho VUIHOC | `https://insight-os-api.vuihoc.vn/mcp` | Claude + Codex + Cursor |
| [`rino-insight-os`](./plugins/rino-insight-os) | `0.2.0` | Customer context, sales coaching, market và conversion intelligence có evidence cho Rino Edu | `https://insight-os-api.rinoedu.ai/mcp` | Claude + Codex + Cursor |
| [`lms-review`](./plugins/lms-review) | `0.1.0` | Review dữ liệu LMS revise/practice qua MCP VUIHOC | `https://dev-mcp.vuihoc.vn/lms` | Codex only |

---

## Cài đặt nhanh (Dành cho cả người không chuyên kỹ thuật)

### Cách 1: Copy Prompt nhờ AI tự cài đặt

Chỉ cần sao chép đoạn nhắc dưới đây và dán vào khung chat của AI (Claude Code, Cursor, Codex, Windsurf, Gemini CLI, OpenCode…), thay `<tên-plugin>` bằng tên plugin muốn cài (ví dụ `vuihoc-content-authoring`):

```text
Hãy giúp mình cài đặt plugin "vuihoc-content-authoring" từ kho GitHub https://github.com/vuihoc-edtech/rnd-plugins (thư mục plugins/vuihoc-content-authoring) theo đúng môi trường bạn đang chạy:
- Claude Code: chạy `claude plugin marketplace add vuihoc-edtech/rnd-plugins` và `claude plugin install vuihoc-content-authoring@vuihoc-rnd`.
- Codex: chạy `codex plugin marketplace add https://github.com/vuihoc-edtech/rnd-plugins.git` và `codex plugin add vuihoc-content-authoring@vuihoc-rnd`.
- Cursor / Windsurf / Gemini CLI / Agent khác: chạy `npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g -y` và thêm MCP server trong file `.mcp.json` của plugin vào cấu hình MCP của bạn.
Cài xong hãy hướng dẫn mình bước tiếp theo bằng tiếng Việt dễ hiểu.
```

### Cách 2: Cài trên `claude.ai` / Claude Desktop / Cowork (Giao diện đồ họa)

1. Mở **[claude.ai/customize/plugins](https://claude.ai/customize/plugins)** (hoặc mở **Claude Desktop** → **Customize** → **Plugins**).
2. Bấm **Add > Add marketplace**, dán URL:
   ```text
   https://github.com/vuihoc-edtech/rnd-plugins
   ```
3. Chọn plugin cần dùng (ví dụ **Soạn học liệu VUIHOC**) → bấm **Add**.
4. Mở tab **Connectors** trong trang chi tiết của plugin → bấm **Connect** và đăng nhập tài khoản VUIHOC SSO.

### Cách 3: Cài trên Claude Code (CLI / IDE)

```bash
# Cài trực tiếp 1 bước (Claude Code >= 2.1.275)
/plugin install vuihoc-content-authoring --marketplace vuihoc-edtech/rnd-plugins

# Hoặc thêm marketplace trước rồi cài từng plugin
/plugin marketplace add vuihoc-edtech/rnd-plugins
/plugin install vuihoc-content-authoring@vuihoc-rnd
/plugin install mark-flow@vuihoc-rnd
/plugin install insight-os@vuihoc-rnd
```

### Cách 4: Cài trên OpenAI Codex

```bash
codex plugin marketplace add https://github.com/vuihoc-edtech/rnd-plugins.git
codex plugin add vuihoc-content-authoring@vuihoc-rnd
```

### Cách 5: Cài kỹ năng cho mọi Agent qua `npx skills`

```bash
npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g
```

---

## Quản lý Phiên bản (Version Management)

Repo sử dụng công cụ `scripts/plugin_versions.py` để đồng bộ phiên bản SemVer trên toàn bộ các manifest (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`) và kiểm tra tính toàn vẹn của marketplace:

```bash
# 1. Xem phiên bản hiện tại của tất cả plugin
python3 scripts/plugin_versions.py status

# 2. Kiểm tra đồng bộ version, đường dẫn marketplace và file rác (.DS_Store)
python3 scripts/plugin_versions.py check

# 3. Tăng version cho một plugin (patch | minor | major hoặc --set X.Y.Z)
python3 scripts/plugin_versions.py bump vuihoc-content-authoring patch

# 4. Validate với bộ công cụ chuẩn trước khi push
claude plugin validate --strict .
claude plugin validate --profile directory --strict plugins/vuihoc-content-authoring
```

---

## Quy tắc Khai báo MCP (Tránh lỗi Sync trên Claude Desktop / claude.ai)

> **Tuyệt đối không tạo `.claude-plugin/mcp.json` khác nội dung với `.mcp.json`.**
> Validator phía server của `claude.ai` / Claude Desktop đọc cả `.mcp.json` và `.claude-plugin/mcp.json`. Nếu cùng một tên MCP server xuất hiện ở hai file với nội dung khác nhau, toàn bộ marketplace sẽ bị từ chối đồng bộ (`MARKETPLACE_ERROR:REMOTE_SYNC_FAILED`).

Quy chuẩn trong repo này:
1. **Claude**: Khai báo `mcpServers` **inline** ngay trong `.claude-plugin/plugin.json` (không tạo `.claude-plugin/mcp.json`).
2. **Codex & Cursor**: Đọc từ `.mcp.json` ở gốc thư mục từng plugin với cấu trúc `{"mcpServers": {"<server>": {"type": "http", "url": "..."}}}` đồng nhất với khai báo inline của Claude.

## Liên hệ

Team R&D — VUIHOC (`https://vuihoc.vn/`)
