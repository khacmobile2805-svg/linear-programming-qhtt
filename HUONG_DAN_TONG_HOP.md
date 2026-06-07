# HƯỚNG DẪN ĐẦY ĐỦ — CHƯƠNG TRÌNH GIẢI QHTT TỔNG QUÁT

> Dành cho người mới bắt đầu với Python và VS Code.
> Bao gồm: cấu trúc dự án, 3 phương pháp được cài đặt, cách chạy web.

---

## 1. BA PHƯƠNG PHÁP ĐƯỢC CÀI ĐẶT

| Ký hiệu | Tên trong vở | Vị trí trong code |
|---|---|---|
| **④** | Giải QHTT 2 biến bằng **phương pháp hình học** | `backend/core/geometry.py` |
| **⑥** | Phương pháp **đơn hình dạng từ vựng** | `backend/core/simplex.py`, `two_phase.py` |
| **⑧** | Giải QHTT **suy biến — quy tắc Bland** | tham số `rule='bland'` trong simplex |

---

## 2. CẤU TRÚC DỰ ÁN

```
LinearProgramming/
│
├── app.py                  ← CHẠY FILE NÀY để mở web
├── demo.py                 ← Chạy demo dòng lệnh (in từ vựng)
├── test_cases.py           ← Kiểm thử tự động (10 ca)
├── requirements.txt        ← Thư viện cần cài: streamlit, matplotlib, numpy
│
└── backend/
    ├── models/             ← Các lớp dữ liệu
    │   ├── variable.py     (VariableSign, Variable)
    │   ├── constraint.py   (ConstraintOp, Constraint)
    │   ├── objective.py    (ObjectiveSense, Objective)
    │   ├── problem.py      (Problem — bài toán tổng quát)
    │   └── standard_problem.py  (StandardProblem — dạng chuẩn min)
    │
    ├── core/               ← Thuật toán
    │   ├── standardizer.py (đưa tổng quát → chuẩn min)
    │   ├── simplex.py      ⑥⑧ (Dictionary, pivot, Dantzig/Bland)
    │   ├── two_phase.py    ⑨  (điều phối 2 pha)
    │   ├── solver.py           (API cấp cao: solve(...))
    │   └── geometry.py     ④  (vẽ miền nghiệm, tịnh tiến mục tiêu)
    │
    └── utils/
        └── formatting.py   (fmt — hiển thị phân số)
```

---

## 3. CÀI ĐẶT MÔI TRƯỜNG (làm 1 lần)

### Bước 1 — Cài Python
- Vào https://python.org/downloads → tải bản mới nhất.
- **Windows: TÍCH "Add Python to PATH"** rồi mới bấm Install.
- Kiểm tra (mở Command Prompt):
  ```
  python --version
  ```

### Bước 2 — Cài Visual Studio Code
- Vào https://code.visualstudio.com → tải và cài.
- Mở VS Code → **Extensions** (Ctrl+Shift+X) → tìm **"Python"** → Install.

### Bước 3 — Mở dự án trong VS Code
1. Giải nén `LinearProgramming.zip` ra Desktop (hoặc bất cứ đâu).
2. VS Code → **File → Open Folder** → chọn thư mục `LinearProgramming`.
3. Thanh bên trái sẽ hiện đúng cây thư mục như mục 2 ở trên.

### Bước 4 — Cài các thư viện cần thiết
Trong VS Code, bấm **Ctrl + `** (dấu backtick) để mở Terminal bên dưới, rồi gõ:
```
pip install streamlit matplotlib numpy
```
Chờ tải xong (1–2 phút).

---

## 4. CHẠY WEB (3 cách)

### Cách A — Chạy bằng Terminal trong VS Code ✅ (khuyên dùng)
Trong Terminal VS Code (Ctrl + `), đảm bảo đang ở thư mục `LinearProgramming`:
```
streamlit run app.py
```
Trình duyệt tự mở ở `http://localhost:8501`. 🎉

### Cách B — Bấm nút ▶ trong VS Code
1. Mở file `app.py`.
2. Góc phải trên có nút ▶ (Run) — **KHÔNG dùng cách này** vì VS Code chạy `python app.py`, không phải `streamlit run app.py`. Sẽ lỗi. Dùng Terminal thay.

### Cách C — Chạy từ Windows Explorer
Mở thư mục `LinearProgramming` → gõ `cmd` vào thanh địa chỉ → Enter → gõ:
```
streamlit run app.py
```

> ⚠️ **Lỗi "No module named 'backend'":** bạn đang chạy sai thư mục. Phải đứng trong `LinearProgramming` (chỗ thấy `app.py`).

---

## 5. CÁCH DÙNG WEB — TỪNG BƯỚC

### Nhập bài toán
1. **Thanh bên trái (sidebar):**
   - Chọn **Nạp ví dụ mẫu** để dùng ngay, hoặc tự nhập.
   - Chọn số biến, số ràng buộc, max/min.
   - **⑧ Quy tắc:** chọn `Bland` nếu nghi bài suy biến (muốn đảm bảo không xoay vòng).
   - Tích **④ Vẽ miền nghiệm** nếu bài có 2 biến.
   - Tích **⑥ Hiển thị các từ vựng** để xem bảng từng bước.

2. **Mục 1:** nhập hệ số hàm mục tiêu (c₁, c₂, …).
3. **Mục 2:** nhập từng ràng buộc — hệ số, chọn dấu `≤ / ≥ / =`, vế phải.
4. **Mục 3:** chọn dấu mỗi biến: `x ≥ 0`, `x ≤ 0`, hoặc `tự do`.
5. Bấm **🚀 GIẢI BÀI TOÁN**.

### Đọc kết quả
- **Giá trị tối ưu z\***: số tối ưu.
- **Nghiệm**: x₁, x₂, … đạt giá trị đó.
- Cảnh báo **suy biến** (⑧) nếu có biến cơ sở = 0.
- **④ Biểu đồ hình học**: miền xanh = miền chấp nhận được, ★ = điểm tối ưu, nét đứt = đường mức z*.
- **⑥ Từ vựng**: mở từng bước, xem từ vựng trước và sau mỗi phép xoay.
- 🔸 `suy biến` trên tiêu đề bước = bước suy biến (tỉ số = 0).

---

## 6. DEMO VÀ KIỂM THỬ BẰNG LỆNH

```bash
# Chạy demo in từ vựng ra màn hình (3 ví dụ)
python demo.py

# Chạy kiểm thử tự động (10 ca, kiểm chứng đáp án)
python test_cases.py
```

---

## 7. LÝ THUYẾT TÓM TẮT CÁC PHƯƠNG PHÁP

### ④ Phương pháp hình học (`geometry.py`)
- Chỉ dùng cho **2 biến**.
- Vẽ miền chấp nhận được (giao các nửa mặt phẳng ràng buộc).
- **Tịnh tiến đường mức** `z = const` theo hướng tối ưu đến điểm cuối cùng còn chạm miền.
- Đỉnh đó = nghiệm tối ưu.

### ⑥ Đơn hình dạng từ vựng (`simplex.py`, `two_phase.py`)
- Đưa bài về **dạng chuẩn min**: `min cᵀx, Ax ≤ b, x ≥ 0`.
- Từ vựng: `wᵢ = bᵢ − Σaᵢⱼxⱼ`, `z = Σcⱼxⱼ`.
- **Biến vào**: hệ số âm nhất trên dòng z (Dantzig).
- **Biến ra**: tỉ số nhỏ nhất `min{bᵢ/aᵢⱼ : aᵢⱼ > 0}`.
- Dừng khi mọi hệ số dòng z ≥ 0.
- Nếu có bᵢ < 0: dùng **2 pha** (bài bổ trợ min x₀).

### ⑧ Quy tắc Bland và suy biến (`simplex.py` — tham số `rule='bland'`)
- **Suy biến**: khi bᵢ = 0 tại một đỉnh — có thể gây xoay vòng vô hạn nếu dùng Dantzig.
- **Quy tắc Bland** (chống cycling): chọn **biến vào = biến phi cơ sở có chỉ số nhỏ nhất** trong số các cột có hệ số âm trên dòng z (thay vì âm nhất).
- Bland **đảm bảo thuật toán luôn dừng** sau hữu hạn bước.

---

## 8. MỘT SỐ LỖI THƯỜNG GẶP

| Lỗi | Nguyên nhân | Cách sửa |
|---|---|---|
| `No module named 'backend'` | Sai thư mục chạy | `cd LinearProgramming` trước khi chạy |
| `streamlit: command not found` | Chưa cài hoặc thiếu PATH | `pip install streamlit` |
| `No module named 'matplotlib'` | Chưa cài | `pip install matplotlib numpy` |
| Web không tự mở | Streamlit đã chạy | Tự copy `http://localhost:8501` vào trình duyệt |
| Cổng 8501 đã dùng | App khác đang chạy | Thêm `--server.port 8502` vào lệnh |

---

## 9. NỘP BÀI

Yêu cầu Moodle — nộp **2 file**:

1. **Báo cáo PDF**: đặt tên `Tên nhóm - K23 - Ngành.pdf` (mở `BaoCao_template.docx`, điền thông tin, xuất PDF).
2. **Mã nguồn nén**: nén thư mục `LinearProgramming` thành `.zip` hoặc `.rar`.

**Hạn nộp: 11/06/2026, 23h55.**
