# Soạn học liệu VUIHOC (`vuihoc-content-authoring`)

**Phiên bản hiện tại:** `1.0.0` · **Hỗ trợ:** Claude (`claude.ai`, Claude Desktop, Cowork, Claude Code), OpenAI Codex & ChatGPT, Cursor, Windsurf, Gemini CLI, VS Code Copilot và mọi AI Agent hỗ trợ chuẩn MCP / Agent Skills.

Plugin giúp thầy/cô giáo viên VUIHOC soạn câu hỏi LMS ngay trong trợ lý AI quen dùng của mình. Câu hỏi do AI soạn được ghi thẳng vào **bản nháp** trên ứng dụng [Soạn học liệu VUIHOC](https://docx-converter.vuihoc.vn) — thầy/cô mở link phiên để xem, sửa tay, tạo giọng đọc (voice) và nạp lên LMS.

---

## Trọn bộ tính năng trong Plugin

1. **Kết nối máy chủ MCP `vuihoc-author`** (`https://docx-converter.vuihoc.vn/mcp`):
   - Đăng nhập trực tiếp bằng **tài khoản VUIHOC (SSO)** trên trình duyệt khi kết nối lần đầu — **không cần xin hay dán token thủ công**.
2. **Bộ 4 kỹ năng chuyên biệt (`skills/`)**:
   - `draft-questions`: Mở mới hoặc tìm lại phiên đang soạn dở, chốt yêu cầu (môn, lớp, chủ đề, ma trận, dạng câu, tài liệu đính kèm) và điều phối soạn từng đợt 1–2 câu.
   - `soan-cau-hoi`: Quy chuẩn soạn câu hỏi VUIHOC theo GDPT 2018 (TN1, TNN, DS, DS4, DK, KT, VO; mức NB, TH, VD, VDC), bắt buộc AI tự giải độc lập trước khi cài đáp án (kèm hướng dẫn riêng cho Tiếng Anh, Tiếng Việt, Ngữ văn).
   - `kiem-chung-toan`: Giải kiểm chứng bằng Python + `sympy` cho các câu Toán/tính toán mức VD, VDC (tối ưu, hình học, làm tròn sách giáo khoa, đọc số kiểu Việt Nam `60.000`, `0,175`).
   - `check-draft`: Rà soát toàn bộ bản nháp, báo cáo tiến độ ma trận, các câu còn lỗi hoặc gắn cờ cần kiểm và sửa từng câu mà không ghi đè phần thầy/cô đã sửa tay.
3. **Lệnh tắt (Slash Commands)**:
   - `/vuihoc-content-authoring:soan-cau-hoi`: Bắt đầu hoặc tiếp tục soạn câu hỏi.
   - `/vuihoc-content-authoring:kiem-tra-nhap`: Kiểm tra bản nháp và tiến độ ma trận.

---

## Cách 1: Giao cho AI tự cài đặt (Nhanh & dễ nhất — khuyên dùng)

Nếu thầy/cô đang dùng **Claude Code, Cursor, Codex, Windsurf, Gemini CLI, OpenCode…**, không cần tự gõ lệnh kỹ thuật. Hãy **sao chép nguyên đoạn chữ dưới đây** và dán vào khung chat của trợ lý AI:

```text
Hãy cài đặt plugin và kết nối MCP "Soạn học liệu VUIHOC" (vuihoc-content-authoring) cho tôi theo đúng môi trường bạn đang chạy:

1. Nguồn plugin:
   - Kho GitHub: https://github.com/vuihoc-edtech/rnd-plugins
   - Thư mục plugin: plugins/vuihoc-content-authoring
   - Máy chủ MCP: tên "vuihoc-author", giao thức Streamable HTTP, địa chỉ: https://docx-converter.vuihoc.vn/mcp

2. Cách cài tự động theo công cụ của bạn:
   - Nếu bạn là Claude Code: chạy `claude plugin marketplace add vuihoc-edtech/rnd-plugins` rồi `claude plugin install vuihoc-content-authoring@vuihoc-rnd` (hoặc thêm MCP bằng `claude mcp add --transport http -s user vuihoc-author https://docx-converter.vuihoc.vn/mcp` và cài kỹ năng bằng `npx -y skills add vuihoc-edtech/rnd-plugins/plugins/vuihoc-content-authoring -g -a claude-code -y`).
   - Nếu bạn là OpenAI Codex: chạy `codex plugin marketplace add https://github.com/vuihoc-edtech/rnd-plugins.git` rồi cài `vuihoc-content-authoring@vuihoc-rnd` (hoặc khai báo `mcp_servers.vuihoc-author` với `url = "https://docx-converter.vuihoc.vn/mcp"` trong `~/.codex/config.toml` và chạy `npx -y skills add vuihoc-edtech/rnd-plugins/plugins/vuihoc-content-authoring -g -a codex -y`).
   - Nếu bạn là Cursor / Windsurf / VS Code / OpenCode / Agent khác: cài bộ kỹ năng bằng `npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g -y`, đồng thời thêm máy chủ MCP HTTP `"vuihoc-author": { "type": "http", "url": "https://docx-converter.vuihoc.vn/mcp" }` vào file cấu hình MCP của bạn.
   - Nếu bạn là Gemini CLI: chạy `gemini mcp add -t http -s user vuihoc-author https://docx-converter.vuihoc.vn/mcp` và `npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g -a gemini-cli -y`.

3. Sau khi cài xong, hãy báo lại cho tôi bằng tiếng Việt dễ hiểu và hướng dẫn tôi bấm đăng nhập tài khoản VUIHOC SSO để bắt đầu soạn câu hỏi.
```

---

## Cách 2: Cài đặt thủ công theo từng ứng dụng

### A. Claude trên Web & Máy tính (`claude.ai`, Claude Desktop, Cowork)

Phù hợp nhất cho thầy/cô dùng Claude trực tiếp trên trình duyệt hoặc ứng dụng Claude trên máy tính (tài khoản Pro, Max, Team, Enterprise):

#### Cách A1 — Cài trọn bộ từ Kho Plugin (Khuyên dùng, có đủ cả Kết nối + 4 Kỹ năng)

1. Mở trang **[claude.ai/customize/plugins](https://claude.ai/customize/plugins)** (hoặc mở ứng dụng **Claude Desktop** → chọn mục **Customize** ở thanh bên trái → chọn **Plugins**).
2. Bấm nút **Add** → chọn **Add marketplace**, rồi dán địa chỉ kho plugin của VUIHOC:
   ```text
   https://github.com/vuihoc-edtech/rnd-plugins
   ```
3. Tìm **Soạn học liệu VUIHOC** (`vuihoc-content-authoring`) trong danh sách → bấm **Add** để cài vào tài khoản.
4. Bấm vào plugin **Soạn học liệu VUIHOC** vừa cài → mở tab **Connectors** → tại dòng `vuihoc-author`, bấm **Connect**.
5. Trình duyệt mở trang xin phép → bấm **Cho phép** → đăng nhập bằng **tài khoản VUIHOC (SSO)**.
6. Mở cuộc trò chuyện mới và nhắn thử: *"Soạn cho mình 2 câu hỏi Toán lớp 6 bài Phép cộng phân số"*.

> **Mẹo:** Trong **Settings > Capabilities** của Claude, hãy bật tính năng **Code execution (Thực thi mã)** để Claude tự chạy Python kiểm chứng đáp án các câu Toán khó.

#### Cách A2 — Chỉ nối nhanh qua Custom Connector (Nếu không dùng kho Plugin)

1. Vào **Settings (hoặc Customize) > Connectors > Add custom connector**.
2. Dán địa chỉ máy chủ MCP:
   ```text
   https://docx-converter.vuihoc.vn/mcp
   ```
3. Bấm **Connect** → chọn **Cho phép** → đăng nhập bằng **tài khoản VUIHOC (SSO)**.

---

### B. Claude Code (CLI / VS Code / JetBrains / Desktop Code)

Chạy lệnh một bước ngay trong khung chat của Claude Code:

```text
/plugin install vuihoc-content-authoring --marketplace vuihoc-edtech/rnd-plugins
```

*(Hoặc thêm kho trước rồi cài:*
```text
/plugin marketplace add vuihoc-edtech/rnd-plugins
/plugin install vuihoc-content-authoring@vuihoc-rnd
```
*)*

Sau khi cài:
1. Chạy `/reload-plugins` (hoặc khởi động lại phiên).
2. Gõ `/mcp` → chọn `vuihoc-author` → trình duyệt tự mở để thầy/cô bấm **Cho phép** và đăng nhập **SSO VUIHOC**.

---

### C. ChatGPT & OpenAI Codex (ChatGPT Desktop / Web, Codex CLI)

#### Trên ChatGPT Web / Desktop (Qua Connector)
1. Mở **Settings > Apps & Connectors** (hoặc **Connectors**) → chọn **Add custom MCP server / Create connector**.
2. Điền địa chỉ máy chủ MCP:
   ```text
   https://docx-converter.vuihoc.vn/mcp
   ```
3. Bấm kết nối, chọn **Cho phép** và đăng nhập bằng **tài khoản VUIHOC (SSO)**.

#### Trên OpenAI Codex (Codex CLI & ChatGPT Desktop Work Mode)
1. Thêm kho plugin của VUIHOC trong Terminal:
   ```bash
   codex plugin marketplace add https://github.com/vuihoc-edtech/rnd-plugins.git
   codex plugin add vuihoc-content-authoring@vuihoc-rnd
   ```
2. Đăng nhập MCP:
   ```bash
   codex mcp login vuihoc-author
   ```

---

### D. Cursor, Windsurf, Gemini CLI & Các AI Agent khác

#### 1. Trên Cursor IDE
- **Cách 1 (Cài từ Marketplace):** Thêm kho `https://github.com/vuihoc-edtech/rnd-plugins` vào mục **Plugins** của Cursor và bật **Soạn học liệu VUIHOC**.
- **Cách 2 (Cài kỹ năng + MCP):**
  Chạy lệnh cài bộ 4 kỹ năng vào Cursor:
  ```bash
  npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g -a cursor -y
  ```
  Và thêm vào `~/.cursor/mcp.json`:
  ```json
  {
    "mcpServers": {
      "vuihoc-author": {
        "type": "http",
        "url": "https://docx-converter.vuihoc.vn/mcp"
      }
    }
  }
  ```

#### 2. Trên Gemini CLI
```bash
gemini extensions install https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring --consent
```
Hoặc thêm MCP + kỹ năng:
```bash
gemini mcp add -t http -s user vuihoc-author https://docx-converter.vuihoc.vn/mcp
npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g -a gemini-cli -y
```

#### 3. Cài đặt đa nền tảng (Hơn 70 AI Agent qua `npx skills`)
Mọi công cụ hỗ trợ chuẩn Agent Skills (Windsurf, GitHub Copilot, Cline, Roo Code, OpenCode…) đều cài được bộ kỹ năng bằng 1 dòng lệnh:
```bash
npx -y skills add https://github.com/vuihoc-edtech/rnd-plugins/tree/main/plugins/vuihoc-content-authoring -g
```
Sau đó nối MCP server với địa chỉ `https://docx-converter.vuihoc.vn/mcp` trong phần cài đặt MCP của ứng dụng.

---

## Quản lý & Cập nhật phiên bản (Version Management)

### Dành cho Giáo viên / Người dùng

Khi VUIHOC nâng cấp kỹ năng soạn câu hỏi hoặc bổ sung tính năng mới:

- **Trên `claude.ai` / Claude Desktop / Cowork**: Mở **Customize > Plugins**, chọn kho `vuihoc-rnd` và bấm **Check for updates** (hoặc bật **Sync automatically** để tự động cập nhật).
- **Trên Claude Code**: Gõ `/plugin update vuihoc-content-authoring` rồi `/reload-plugins`.
- **Trên Codex**: Chạy `codex plugin marketplace upgrade vuihoc-rnd`.
- **Nếu cài qua `npx skills`**: Chạy `npx skills update -g`.
- **Hoặc nhắn trực tiếp cho AI**: *"Hãy cập nhật plugin vuihoc-content-authoring của mình lên bản mới nhất"*.

Xem lịch sử thay đổi chi tiết tại [CHANGELOG.md](./CHANGELOG.md).

### Dành cho Đội phát triển (Maintainers)

Plugin lưu trữ version đồng bộ trên 4 manifest (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`). Luôn sử dụng công cụ quản lý version ở gốc repo trước khi push:

```bash
# Xem trạng thái version của tất cả plugin
python3 scripts/plugin_versions.py status

# Tăng version (patch / minor / major) đồng bộ trên mọi manifest
python3 scripts/plugin_versions.py bump vuihoc-content-authoring patch

# Kiểm tra tính hợp lệ và đồng bộ
python3 scripts/plugin_versions.py check
claude plugin validate --profile directory --strict plugins/vuihoc-content-authoring
claude plugin validate --strict .
gemini extensions validate plugins/vuihoc-content-authoring
```

---

## Quy trình làm việc của Giáo viên sau khi soạn

1. **Soạn từng đợt trong AI**: Mỗi lượt AI tự giải kiểm chứng và ghi tối đa 2 câu vào bản nháp, kèm đường link tới phiên soạn.
2. **Duyệt và nạp LMS trên Web**: Mở đường link phiên trên ứng dụng web để xem trước câu hỏi, sửa tay nếu cần, bấm **"Xong, tạo voice"** (cho các câu có thẻ `[Voice]`) và bấm **Nhập lên LMS**.

## Quyền riêng tư & Bảo mật dữ liệu (Privacy)

Plugin chỉ kết nối tới máy chủ soạn học liệu chính thức của VUIHOC (`https://docx-converter.vuihoc.vn/mcp`). Dữ liệu gửi đi gồm yêu cầu soạn bài, tài liệu giáo viên cung cấp và nội dung câu hỏi nháp trong phiên của chính giáo viên đó. Xác thực thông qua chuẩn OAuth 2.1 + PKCE đứng trước VUIHOC SSO; plugin không lưu mật khẩu hay token tĩnh. Chính sách bảo mật chung: [https://vuihoc.vn/](https://vuihoc.vn/).
