---
name: kiem-chung-toan
description: Kiểm chứng bằng Python các câu Toán (và bài tính toán khác) mức VD, VDC khó tính khi soạn câu hỏi VUIHOC - bài tối ưu (lớn nhất, nhỏ nhất), hình học, làm tròn, Đúng/Sai, chọn bộ số cho đề - kèm thư viện đọc số kiểu Việt Nam (60.000, 0,175) và làm tròn kiểu sách giáo khoa. Dùng cùng kỹ năng soan-cau-hoi trước khi nộp câu.
---

# Kiểm chứng bài khó

Bổ sung cho phần Kiểm chứng của kỹ năng `soan-cau-hoi`. Cần môi trường chạy Python có `sympy` (`pip install sympy` nếu thiếu). Không chạy được Python thì giải từng bước cẩn thận, thử ngược vào đề, và hạ `confidence` với câu VD, VDC không kiểm được bằng cách thứ hai.

## Thư viện `scripts/vn.py`

Nằm trong thư mục kỹ năng này, tại `scripts/vn.py` (Claude Code: `${CLAUDE_SKILL_DIR}/scripts`). Thêm đường dẫn đầy đủ của thư mục `scripts` vào `sys.path` rồi `from vn import num, rnd`; hoặc dán nội dung file vào đầu lần chạy.

- `num("60.000")` → 60000; `num("0{,}175")` → 7/40; `num("1,5")` → 3/2: số hữu tỉ chính xác từ chuỗi số kiểu Việt Nam.
- `rnd(value, digits)`: làm tròn kiểu sách giáo khoa (năm lên), không dùng `round()`.

Gộp mọi phép tính của một lượt vào **một lần chạy**; số hữu tỉ trước, ra thập phân ở bước cuối.

## Theo loại bài

- Bài tối ưu (lớn nhất, nhỏ nhất): giải đạo hàm **và** quét số trên miền xác định để chắc đó là cực trị toàn cục, kể cả giá trị ở hai đầu mút.
- Bài làm tròn: đáp án theo đúng yêu cầu của đề ("hàng phần mười", "2 chữ số thập phân"); đề phải ghi rõ làm tròn ở đâu.
- Hình học: đặt toạ độ hoặc dùng công thức, rồi kiểm lại bằng một quan hệ khác của hình.
- Đúng/Sai: kiểm từng mệnh đề riêng; một mệnh đề "Đúng" phải đúng với mọi trường hợp đề cho.
- Chọn số cho đề: thử vài bộ dữ kiện bằng Python để kết quả hợp lý (không âm khi đại lượng không thể âm, không ra số quá xấu) rồi mới viết vào đề.
- Không mô hình hoá được bài (đề mơ hồ, thiếu dữ kiện): sửa đề cho rõ, hoặc hạ `confidence` và nói với giáo viên; không cài đáp án đoán.

## Ví dụ bài tối ưu

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "<thư mục kỹ năng>/scripts")   # Claude Code: "${CLAUDE_SKILL_DIR}/scripts"
from vn import num, rnd
from sympy import *
x = symbols("x", positive=True)
S = num("0{,}175") / num("0{,}7")          # 0,25
f = S*num("120.000") + 2*num("0{,}7")*(x + S/x)*num("100.000")
xm = solve(diff(f, x), x); print(xm, [f.subs(x, v) for v in xm])
PY
```
