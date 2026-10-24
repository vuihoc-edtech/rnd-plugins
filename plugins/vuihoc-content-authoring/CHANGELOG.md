# Changelog — `vuihoc-content-authoring`

Mọi thay đổi đáng chú ý của plugin **Soạn học liệu VUIHOC** được ghi lại tại đây theo chuẩn [Semantic Versioning](https://semver.org/lang/vi/).

## [1.0.0] - 2026-10-24

### Thêm mới
- **Hỗ trợ cài đặt trên toàn bộ AI Agent phổ biến**:
  - **Claude** (`claude.ai`, Claude Desktop, Cowork, Claude Code) qua `.claude-plugin/plugin.json` và marketplace `.claude-plugin/marketplace.json`.
  - **OpenAI Codex & ChatGPT Desktop** qua `.codex-plugin/plugin.json`, `.mcp.json`, `skills/*/agents/openai.yaml` và `.agents/plugins/marketplace.json`.
  - **Cursor IDE** qua `.cursor-plugin/plugin.json` và `.cursor-plugin/marketplace.json`.
  - **Gemini CLI** qua `gemini-extension.json` và `GEMINI.md`.
  - **Mọi Agent hỗ trợ chuẩn Agent Skills (Windsurf, VS Code Copilot, Cline, Roo Code, OpenCode...)** qua `npx skills add`.
- **Slash Commands**: `/vuihoc-content-authoring:soan-cau-hoi` và `/vuihoc-content-authoring:kiem-tra-nhap`.
- **Bộ nhận diện (Assets)**: biểu tượng chuẩn `assets/icon.png` (512×512), `assets/icon.svg`, `assets/logo.svg` và `privacyPolicyUrl`.
- **Quản lý phiên bản**: đồng bộ version qua `scripts/plugin_versions.py`.
- **Hướng dẫn cài đặt cho người không chuyên kỹ thuật (Non-tech)**: bổ sung **Prompt mẫu để giao cho AI tự cài đặt** và hướng dẫn từng bước trực quan theo từng ứng dụng.

### Thay đổi
- Chuẩn hoá nội dung 4 kỹ năng (`draft-questions`, `soan-cau-hoi`, `kiem-chung-toan`, `check-draft`) trung tính với mọi trợ lý AI thay vì chỉ nhắc riêng Claude.
- Cập nhật địa chỉ kho lưu trữ chính thức sang `https://github.com/vuihoc-edtech/rnd-plugins`.

## [0.1.0] - 2026-10-21

### Thêm mới
- Phiên bản đầu tiên dành cho Claude: kết nối MCP `vuihoc-author` (`https://docx-converter.vuihoc.vn/mcp`) và 4 kỹ năng `draft-questions`, `soan-cau-hoi`, `kiem-chung-toan`, `check-draft`.
