---
name: check-draft
description: Kiểm tra bản nháp câu hỏi VUIHOC của một phiên soạn - tóm tắt câu lỗi, câu bị gắn cờ cần kiểm, tiến độ ma trận, rồi đề xuất và sửa từng câu. Dùng khi giáo viên nói "kiểm tra bản nháp", "xem lại các câu đã soạn", "còn lỗi gì không", "tiến độ ma trận", "sửa câu số ...".
---

# Kiểm tra bản nháp

Trả lời giáo viên bằng tiếng Việt, ngắn, giọng đồng nghiệp; không nhắc tên công cụ, mã lỗi hay trường kỹ thuật; công thức trong `$...$`; kèm liên kết phiên.

## Các bước

1. Xác định phiên: liên kết/mã giáo viên đưa, hoặc `list_sessions` rồi chọn (hỏi nếu có nhiều phiên khớp; phiên cũ hơn thì gọi tiếp với `offset` là `next_offset`). Chỉ dùng được phiên mở qua kết nối MCP của trợ lý AI (không mở được phiên tạo ở khung chat trên trang web "Soạn với AI").
2. `get_workspace` (phiên hơn 60 câu thì xem thêm trang bằng `page`). Giáo viên có thể đã sửa tay, nên luôn đọc bản mới nhất.
3. Tóm tắt gọn:
   - **Tiến độ ma trận**: đã có bao nhiêu trên tổng, mức/danh mục còn thiếu.
   - **Câu còn lỗi**: số câu, vướng gì, cách sửa.
   - **Câu bị gắn cờ cần kiểm** (độ chắc thấp): vì sao chưa chắc.
   - Nhận xét ngắn về độ đa dạng: dạng câu, mức, danh mục, ý trùng nhau.
4. Đề xuất sửa cụ thể, đánh số theo số câu trong bản nháp. Chỉ sửa khi giáo viên đồng ý (hoặc đã bảo "sửa luôn").

## Sửa một câu

Làm theo luật của kỹ năng `soan-cau-hoi`:

- `revise_question` để lấy câu hiện tại, các lỗi còn tồn và `base_hash`.
- Giải lại độc lập để chắc đáp án, chỉ đổi đúng chỗ cần sửa, **giữ phần giáo viên đã sửa tay**.
- `submit_questions` kèm `replaces` (`question_key`, `base_hash`), đúng một câu mỗi lần. Bị từ chối vì giáo viên vừa sửa (`base_hash` cũ) thì lấy lại câu bằng `revise_question` rồi làm lại trên bản mới, không ghi đè.
- Không sửa nhiều hơn 2 câu mỗi lượt; còn lại đề nghị lượt sau.
- Báo rõ đã đổi gì ở câu nào, hoặc vì sao chưa sửa.

Việc nhập lên LMS do giáo viên làm trong ứng dụng; bạn không nhập.
