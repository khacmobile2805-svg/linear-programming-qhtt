# Chương trình giải bài toán Quy hoạch tuyến tính tổng quát

Ứng dụng web giải bài toán **Quy hoạch tuyến tính (QHTT) tổng quát** bằng phương pháp
**đơn hình dạng từ vựng (dictionary simplex) hai pha**, tính toán bằng **phân số chính xác**
(không sai số làm tròn). Giao diện viết bằng Streamlit.

> **Môn học:** Quy hoạch tuyến tính · **GVHD:** Assoc. Prof. Nguyễn Lê Hoàng Anh
> **Sinh viên:** Nguyễn Khắc Trọng — 23110217 · Khoa Toán – Tin học, Trường ĐH KHTN – ĐHQG TP.HCM

---

## 1. Tính năng

- Giải bài toán `max`/`min` với **số biến và số ràng buộc tùy ý**.
- Ràng buộc đủ ba dạng: **≤, ≥, =**.
- Biến đủ ba loại dấu: **x ≥ 0, x ≤ 0, tự do**.
- Xuất **nghiệm tối ưu**, **giá trị tối ưu** và **các từ vựng từng bước** (bật/tắt).
- Nhận diện **vô nghiệm**, **không giới nội**, **vô số nghiệm**, **suy biến**.
- **Nhập hệ số dạng phân số** (ví dụ `1/3`, `-2/5`).
- **Kiểm chứng nghiệm** (thay vào ràng buộc gốc), **quy tắc Bland** chống xoay vòng.
- **Vẽ miền nghiệm hình học** khi bài toán có 2 biến.

---

## 2. Yêu cầu

- **Python 3.9** trở lên. Kiểm tra: `python --version`.
- Các thư viện trong `requirements.txt` (Streamlit, matplotlib, numpy).

---

## 3. Cài đặt và chạy

Mở terminal **trong thư mục dự án** (thư mục chứa `app.py`):

```bash
# Bước 1 — cài thư viện (chỉ làm lần đầu)
python -m pip install -r requirements.txt

# Bước 2 — chạy chương trình
python -m streamlit run app.py
```

Trình duyệt tự mở tại `http://localhost:8501`. Dừng chương trình: nhấn **Ctrl + C**.

> Dùng `python -m streamlit ...` thay cho `streamlit ...` để tránh lỗi
> *"streamlit is not recognized"*. Nếu `python` không chạy, thử `py` thay cho `python`.

---

## 4. Hướng dẫn sử dụng

1. Chọn **số biến n**, **số ràng buộc m** và **hướng tối ưu** (max/min).
2. Nhập **hệ số hàm mục tiêu** (có thể nhập phân số như `1/3`).
3. Nhập **hệ số ràng buộc**, chọn **dấu** (≤ ≥ =) và **vế phải**.
4. Chọn **điều kiện dấu** cho từng biến (≥ 0, ≤ 0, tự do).
5. Nhấn **Giải bài toán**.

**Kết quả** gồm: trạng thái (tối ưu / vô nghiệm / không giới nội), giá trị tối ưu z*,
bảng nghiệm, kiểm chứng nghiệm, miền nghiệm hình học (khi n = 2) và các từ vựng từng bước.

---

## 5. Cấu trúc dự án

```
LinearProgramming/
├── app.py                 # Giao diện web (Streamlit)
├── demo.py                # Chạy thử trên dòng lệnh
├── test_cases.py          # 10 ca kiểm thử tự động
├── requirements.txt
├── .streamlit/config.toml # Cấu hình giao diện
└── backend/
    ├── models/            # Variable, Constraint, Objective, Problem
    ├── core/
    │   ├── standardizer.py # đưa về dạng chuẩn MIN
    │   ├── simplex.py      # từ vựng + phép xoay (Dantzig/Bland)
    │   ├── two_phase.py    # đơn hình 2 pha
    │   ├── solver.py       # API cấp cao
    │   └── geometry.py     # vẽ miền nghiệm 2 biến
    └── utils/formatting.py # định dạng phân số
```

---

## 6. Kiểm thử

```bash
python test_cases.py     # 10 ca kiểm thử, kỳ vọng "10/10 test ĐẠT"
python demo.py           # in lời giải + các từ vựng từng bước
```

---

## 7. Triển khai trực tuyến (tùy chọn)

1. Đẩy mã nguồn lên GitHub: `git add . && git commit -m "..." && git push`.
2. Vào [share.streamlit.io](https://share.streamlit.io) → chọn repo, branch `main`,
   Main file `app.py` → **Deploy**.
3. Khi cập nhật code: chỉ cần `git push`, ứng dụng sẽ tự build lại.

---

## 8. Tài liệu tham khảo

- Phan Quốc Khánh, Trần Huệ Nương, *Quy hoạch tuyến tính (Giáo trình hoàn chỉnh)*, Nhà xuất bản Giáo dục.
- Bài giảng và ghi chép trên lớp, học phần Quy hoạch tuyến tính (GV: Assoc. Prof. Nguyễn Lê Hoàng Anh), Khoa Toán – Tin học, Trường ĐH KHTN – ĐHQG TP.HCM.
- R. G. Bland, "New finite pivoting rules for the simplex method," *Mathematics of Operations Research*, 2(2):103–107, 1977.
- Tài liệu Streamlit (https://docs.streamlit.io) và Python (https://docs.python.org).