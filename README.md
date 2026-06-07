# Chương trình giải bài toán Quy hoạch tuyến tính (QHTT) tổng quát

Ứng dụng web giải bài toán QHTT tổng quát bằng **phương pháp đơn hình dạng từ vựng (2 pha)**,
xây dựng bằng Python + Streamlit. Tính toán bằng **phân số chính xác** (không làm tròn).

## Tính năng

- Giải bài toán **tổng quát**: mục tiêu `max`/`min`, số biến và số ràng buộc tùy ý.
- Hỗ trợ ràng buộc dạng `≤`, `≥`, `=`; biến `≥ 0`, `≤ 0` hoặc **tự do**.
- Xuất **nghiệm tối ưu**, **giá trị tối ưu** và **các từ vựng từng bước**.
- Nhận diện **vô nghiệm**, **không giới nội**, **vô số nghiệm**, **suy biến**.
- **Quy tắc Bland** chống xoay vòng vô hạn (tùy chọn).
- **Vẽ miền nghiệm hình học** khi bài toán có đúng 2 biến.

## Cấu trúc dự án

```
LinearProgramming/
├── app.py                      # Giao diện web (Streamlit)
├── demo.py                     # Chạy thử trên dòng lệnh
├── test_cases.py               # Bộ kiểm thử tự động
├── requirements.txt            # Thư viện: streamlit, matplotlib, numpy
└── backend/
    ├── models/                 # Lớp dữ liệu (Variable, Constraint, Objective, Problem)
    ├── core/                   # Thuật toán
    │   ├── standardizer.py     #   đưa về dạng chuẩn MIN
    │   ├── simplex.py          #   từ vựng + phép xoay (Dantzig/Bland)
    │   ├── two_phase.py        #   đơn hình 2 pha
    │   ├── solver.py           #   API cấp cao
    │   └── geometry.py         #   vẽ miền nghiệm 2 biến
    └── utils/
        └── formatting.py       # định dạng phân số
```

## Hướng dẫn chạy (chi tiết)

> Yêu cầu: đã cài **Python 3.9 trở lên**. Kiểm tra bằng cách mở terminal gõ:
> `python --version` — nếu hiện số phiên bản là được. Chưa có thì tải tại
> [python.org/downloads](https://www.python.org/downloads/) (khi cài nhớ tích
> **"Add Python to PATH"**).

**Bước 1 — Mở dự án.** Mở **VS Code** → menu **File → Open Folder…** → chọn thư mục
`LinearProgramming` (thư mục có chứa `app.py`).

**Bước 2 — Mở Terminal.** Trong VS Code, menu **Terminal → New Terminal**. Dòng lệnh
sẽ tự đứng ở đúng thư mục dự án.

**Bước 3 — Cài thư viện** (chỉ cần làm lần đầu):

```bash
pip install -r requirements.txt
```

**Bước 4 — Chạy chương trình:**

```bash
streamlit run app.py
```

Trình duyệt sẽ **tự mở** tại `http://localhost:8501`. Nếu không tự mở, hãy copy địa
chỉ đó dán vào trình duyệt.

**Dừng chương trình:** quay lại terminal, nhấn **Ctrl + C**.

### Lỗi thường gặp

| Báo lỗi | Cách xử lý |
|---|---|
| `'streamlit' is not recognized` / `command not found` | Chạy bằng: `python -m streamlit run app.py` |
| `'pip' is not recognized` | Chạy bằng: `python -m pip install -r requirements.txt` |
| `can't open file 'app.py'` | Đang sai thư mục — dùng `cd` vào đúng thư mục chứa `app.py` rồi chạy lại |
| `ModuleNotFoundError: No module named 'backend'` | Phải chạy lệnh tại thư mục gốc (nơi có `app.py` và thư mục `backend`), không chạy bên trong `backend` |

## Kiểm thử (tùy chọn)

```bash
python test_cases.py     # chạy 10 ca kiểm thử tự động
python demo.py           # in lời giải + các từ vựng từng bước ra màn hình
```

## Triển khai (Streamlit Community Cloud)

1. Đẩy toàn bộ dự án lên GitHub (nên dùng **GitHub Desktop** để giữ đủ cấu trúc thư mục).
2. Vào [share.streamlit.io](https://share.streamlit.io) → **Create app** → chọn repo →
   **Main file path: `app.py`** → **Deploy**.

## Phương pháp

Đơn hình dạng từ vựng, quy về dạng chuẩn MIN; biến bù `w₁…wₘ`, biến phụ pha 1 `x₀`,
mục tiêu phụ `δ`; đơn hình 2 pha khi có `bᵢ < 0`; quy tắc Bland chống xoay vòng.

---
*Học phần Quy hoạch tuyến tính · K23*