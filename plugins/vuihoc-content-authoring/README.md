# Soạn học liệu VUIHOC (Claude)

Plugin cho giáo viên VUIHOC soạn câu hỏi LMS ngay trong Claude (claude.ai web/desktop hoặc Claude Code).

Plugin gồm:

- **Kết nối `vuihoc-author`**: máy chủ MCP của ứng dụng soạn học liệu. Đăng nhập bằng tài khoản VUIHOC (SSO) khi kết nối; không cần dán token.
- **Kỹ năng**:
  - `draft-questions`: bắt đầu hoặc tiếp tục soạn, chọn/tạo phiên, chốt yêu cầu (môn, lớp, chủ đề, ma trận, dạng câu), soạn từng đợt 1-2 câu.
  - `soan-cau-hoi`: tay nghề soạn và vòng làm việc (kèm ghi chú riêng cho Tiếng Anh, Tiếng Việt, Ngữ văn).
  - `kiem-chung-toan`: kiểm chứng bằng Python các câu Toán VD, VDC khó tính.
  - `check-draft`: kiểm tra bản nháp, tóm tắt lỗi, câu cần kiểm, tiến độ ma trận và sửa từng câu.

Câu được ghi thẳng vào **bản nháp** của một phiên trên ứng dụng. Giáo viên xem, sửa tay, tạo voice và **nhập lên LMS trong ứng dụng**; Claude không nhập thay. Mỗi lượt Claude soạn tối đa 2 câu, không soạn tự luận, và không ghi đè phần giáo viên đã sửa.

Chỉ dùng được các phiên tạo từ Claude (qua plugin này); phiên tạo ở trang "Soạn với AI" của ứng dụng không mở được ở đây.

## Cài trong Claude Code

```
/plugin marketplace add vhrnd/plugins
/plugin install vuihoc-content-authoring@vuihoc-rnd
```

Khởi động lại phiên (hoặc `/reload-plugins`), gõ `/mcp`, chọn `vuihoc-author` rồi đăng nhập bằng tài khoản VUIHOC (SSO). Sau đó nói, ví dụ: "Soạn cho mình câu hỏi Toán lớp 6 bài Phép cộng phân số".

## Cài trong claude.ai (web, desktop)

Cần **Owner** của tổ chức thực hiện một lần:

1. **Organization settings > Plugins & skills**: đồng bộ hoặc tải lên plugin này (hoặc tải từng thư mục kỹ năng trong `skills/`).
2. **Connectors > Add custom connector**: thêm máy chủ với URL `https://docx-converter.vuihoc.vn/mcp` (địa chỉ chính thức do nhóm VUIHOC EdTech cung cấp).

Mỗi giáo viên mở Connectors, bấm **Connect** cho kết nối này và đăng nhập bằng SSO VUIHOC, rồi bật các kỹ năng trong phần Skills. Trong cuộc trò chuyện, nhờ Claude "soạn câu hỏi VUIHOC" là kỹ năng tự được dùng.

Với bản chat, nên bật thực thi mã (code execution) để Claude kiểm đáp án bằng Python.

### Tài khoản Claude cá nhân (Pro, Max)

Không cần Owner, mỗi giáo viên tự làm:

1. **Settings > Connectors > Add custom connector**: URL `https://docx-converter.vuihoc.vn/mcp`, bấm **Connect**, cho phép rồi đăng nhập bằng SSO VUIHOC.
2. **Settings > Capabilities**: bật thực thi mã, rồi ở mục **Skills** tải lên từng kỹ năng dạng file zip (mỗi thư mục trong `skills/` nén thành một file, thư mục nằm ở gốc file zip):

```bash
cd plugins/vuihoc-content-authoring/skills
for s in */; do (zip -qr "../${s%/}.zip" "$s"); done
```

## Chạy thử với máy chủ cục bộ

Kết nối của plugin luôn trỏ tới `https://docx-converter.vuihoc.vn/mcp` (claude.ai chỉ nhận URL https cố định). Khi phát triển, thêm một kết nối riêng tới máy chủ cục bộ rồi mở Claude Code kèm thư mục plugin:

```bash
claude mcp add --transport http vuihoc-author-dev http://localhost:5002/mcp
claude --plugin-dir plugins/vuihoc-content-authoring
```

Trong phiên, gõ `/mcp`, chọn `vuihoc-author-dev`, đăng nhập (máy chủ cục bộ dùng trang đăng nhập thử thay cho SSO). Kết nối `vuihoc-author` của plugin sẽ báo cần đăng nhập; bỏ qua nó khi chạy cục bộ. Thử xong thì gỡ: `claude mcp remove vuihoc-author-dev`.

Kiểm tra cấu trúc:

```bash
claude plugin validate plugins/vuihoc-content-authoring
claude plugin validate .
```

## Giáo viên làm tiếp trong ứng dụng

Cuối mỗi lượt Claude gửi liên kết phiên. Mở liên kết để xem các câu vừa soạn, sửa tay, tạo voice (bấm "Xong, tạo voice") và nhập lên LMS. Có thể quay lại Claude bất cứ lúc nào để soạn tiếp hoặc nhờ kiểm tra bản nháp; Claude luôn đọc bản mới nhất, kể cả phần bạn đã sửa.

## Dữ liệu gửi đi

Plugin chỉ nói chuyện với máy chủ soạn học liệu của VUIHOC (`docx-converter.vuihoc.vn`). Những gì gửi tới đó: yêu cầu soạn (môn, lớp, chủ đề, ma trận, ghi chú), tài liệu giáo viên dán vào khi mở phiên và các câu hỏi Claude soạn. Máy chủ lưu chúng trong phiên của giáo viên trên ứng dụng; danh mục câu hỏi được tra từ LMS VUIHOC. Đăng nhập qua SSO VUIHOC; plugin không lưu mật khẩu hay token.

## Kỹ năng kiểm chứng Python

`skills/kiem-chung-toan/scripts/vn.py` cần `sympy` (`pip install sympy`). Không bắt buộc: không có Python thì Claude tự giải từng bước và hạ độ chắc của những câu khó chưa kiểm được.
