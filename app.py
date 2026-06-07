# -*- coding: utf-8 -*-
"""app.py — Giao diện web (phong cách học thuật). Chạy: streamlit run app.py"""
import streamlit as st
from fractions import Fraction

from backend.core.solver import solve
from backend.core.geometry import draw as geo_draw
from backend.utils.formatting import fmt

st.set_page_config(page_title='Quy hoạch tuyến tính', page_icon='∑',
                   layout='wide', initial_sidebar_state='expanded')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Agbalumo&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --ink:#20242b; --ink2:#454b54; --ink3:#717880;
  --paper:#f7f6f2; --line:#e3e0d8; --line2:#eeece6;
  --accent:#0f5d5b; --accent2:#13726f; --accent-lt:#dcefee;
  --green:#15603b; --green-lt:#dcf3e6; --red:#8a2222; --red-lt:#fbe3e3;
  --amber:#7a4a10; --amber-lt:#fbeccd;
}
[data-testid="stAppViewContainer"]{ background:var(--paper); }
[data-testid="stMainBlockContainer"]{ max-width:1080px; padding-top:1.6rem; }
html, body, [class*="css"]{ font-family:'Inter',system-ui,sans-serif; }

/* Masthead — tiêu đề IN HOA font Agbalumo */
.mast{ text-align:center; border-bottom:2px solid var(--ink); padding-bottom:1.1rem; margin-bottom:1.9rem; }
.mast .t{ font-family:'Agbalumo','Source Serif 4',serif; font-size:2.15rem; font-weight:400;
  color:var(--accent); line-height:1.18; text-transform:uppercase; letter-spacing:.005em; margin:0; }
.mast .s{ font-family:'Inter',sans-serif; font-size:.76rem; letter-spacing:.14em; text-transform:uppercase;
  color:var(--ink3); margin-top:.55rem; }

.slabel{ display:flex; align-items:center; gap:.55rem; font-size:.72rem; font-weight:600;
  letter-spacing:.13em; text-transform:uppercase; color:var(--ink3); margin:0 0 .7rem; }
.slabel .n{ display:inline-flex; align-items:center; justify-content:center; width:21px;height:21px;
  border-radius:50%; background:var(--accent); color:#fff; font-size:.68rem; font-weight:700; }
[data-testid="stVerticalBlockBorderWrapper"]{ background:#fff; border-color:var(--line)!important; border-radius:8px!important; }
[data-testid="stNumberInput"] input{ font-family:'JetBrains Mono',monospace!important; text-align:center!important; }
[data-testid="stSidebar"]{ background:var(--ink); }
[data-testid="stSidebar"] *{ color:#dfe3e6!important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{
  color:#fff!important; font-family:'Source Serif 4',serif!important; }
.sb-greek{ font-family:'Agbalumo',serif; font-size:2.4rem; color:rgba(255,255,255,.85); line-height:1; }
.sb-brand{ font-family:'Source Serif 4',serif; font-size:1.4rem; color:#fff; line-height:1.1; }
.sb-desc{ font-size:.72rem; color:rgba(255,255,255,.45); letter-spacing:.04em; }
.sb-h{ font-size:.7rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:rgba(255,255,255,.5); margin:.2rem 0 .4rem;}
.rline{ border-top:2px solid var(--ink); margin:2rem 0 1.2rem; }
.pill{ display:inline-flex; align-items:center; gap:.4rem; font-size:.76rem; font-weight:700;
  letter-spacing:.08em; text-transform:uppercase; padding:5px 14px; border-radius:100px; }
.p-opt{ background:var(--green-lt); color:var(--green);} .p-inf{ background:var(--red-lt); color:var(--red);}
.p-unb{ background:var(--amber-lt); color:var(--amber);}
.rcard{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:1.1rem 1.3rem; }
.rcard .zlb{ font-size:.7rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--ink3);}
.rcard .zv{ font-family:'Source Serif 4',serif; font-size:1.9rem; font-weight:700; color:var(--accent); }
.rtab{ width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:.92rem; margin-top:.3rem;}
.rtab th{ border-bottom:2px solid var(--ink); padding:6px 14px; color:var(--ink2); background:#faf9f6;}
.rtab td{ border-bottom:1px solid var(--line2); padding:7px 14px; text-align:center; color:var(--ink);}
div.stButton>button[kind="primary"]{ background:var(--accent)!important; border:none!important;
  border-radius:6px!important; font-weight:600!important; }
div.stButton>button[kind="primary"]:hover{ background:var(--accent2)!important; }
[data-testid="stExpander"]{ border:1px solid var(--line2)!important; border-radius:6px!important; background:#fff!important;}
h1,h2,h3,h4{ color:var(--ink)!important; } hr{ border-color:var(--line); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="mast">
  <div class="t">Chương trình giải bài toán Quy hoạch tuyến tính tổng quát</div>
  <div class="s">Phương pháp đơn hình dạng từ vựng · 2 pha · Quy tắc Bland · Tính bằng phân số chính xác</div>
</div>
""", unsafe_allow_html=True)

def F(x): return Fraction(str(x))
def slabel(num, text):
    st.markdown(f'<div class="slabel"><span class="n">{num}</span>{text}</div>', unsafe_allow_html=True)

def latex_expr(coeffs):
    terms = []
    for i, c in enumerate(coeffs):
        c = Fraction(str(c))
        if c == 0: continue
        co = '' if abs(c) == 1 else fmt(abs(c))
        t = f"{co}x_{{{i+1}}}"
        terms.append((f"-{t}" if c < 0 else t) if not terms else (f"- {t}" if c < 0 else f"+ {t}"))
    return " ".join(terms) if terms else "0"

def latex_frac(v):
    v = Fraction(v)
    if v.denominator == 1: return str(v.numerator)
    sg = '-' if v < 0 else ''
    return sg + r"\frac{" + str(abs(v.numerator)) + "}{" + str(v.denominator) + "}"

def build_latex_document(sense, obj, constraints, signs, res, rule):
    OPT = {'<=': r'\leq', '>=': r'\geq', '=': '='}
    direction = r'\max' if sense == 'max' else r'\min'
    nn  = [f'x_{{{i+1}}}' for i, s in enumerate(signs) if s == '>=0']
    npz = [f'x_{{{i+1}}}' for i, s in enumerate(signs) if s == '<=0']
    fr  = [f'x_{{{i+1}}}' for i, s in enumerate(signs) if s == 'free']
    sp = []
    if nn:  sp.append(", ".join(nn) + r" \geq 0")
    if npz: sp.append(", ".join(npz) + r" \leq 0")
    if fr:  sp.append(", ".join(fr) + r"\ \text{tự do}")
    sgn = r",\quad ".join(sp)
    lines = [r"& " + direction + r" \; z = " + latex_expr(obj) + r" \\", r"& \text{ràng buộc:} \\"]
    for (co, op, b) in constraints:
        lines.append(r"& \quad " + latex_expr(co) + " " + OPT[op] + " " + latex_frac(b) + r" \\")
    lines.append(r"& \quad " + sgn)
    body = "\n".join(lines)
    status = res['status']
    if status == 'optimal':
        sol = r",\quad ".join(f"x_{{{i+1}}} = " + latex_frac(v) for i, v in enumerate(res['x']))
        rblock = r"\[ z^* = " + latex_frac(res['opt_value']) + r" \]" + "\n" + r"\[ " + sol + r" \]"
    elif status == 'infeasible':
        rblock = r"Bài toán \textbf{vô nghiệm} --- miền ràng buộc rỗng."
    else:
        rblock = r"Bài toán \textbf{không giới nội}."
    steps = ""
    for k, stp in enumerate(res.get('steps', []), 1):
        steps += (r"\textbf{Bước " + str(k) + " --- " + stp['phase'] +
                  " (vào " + stp['enter'] + ", ra " + stp['leave'] + ")}\n")
        steps += r"\begin{verbatim}" + "\n" + stp['dict_before'] + "\n" + r"\end{verbatim}" + "\n\n"
    if status == 'optimal':
        steps += r"\textbf{Từ vựng tối ưu}" + "\n" + r"\begin{verbatim}" + "\n" + res['final_dict'] + "\n" + r"\end{verbatim}" + "\n"
    D = [r"\documentclass[12pt,a4paper]{article}", r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T5]{fontenc}", r"\usepackage[vietnamese]{babel}",
         r"\usepackage{amsmath,amssymb,geometry}", r"\geometry{margin=2.5cm}",
         r"\title{Bài toán Quy hoạch tuyến tính}", r"\date{}", r"\begin{document}", r"\maketitle", "",
         r"\section*{Đề bài}", r"\begin{align*}", body, r"\end{align*}", "",
         r"\section*{Lời giải (đơn hình dạng từ vựng, quy tắc " + rule + ")}", steps,
         r"\section*{Kết quả}", rblock, "", r"\end{document}"]
    return "\n".join(D)

DEF = {'obj':[3,2], 'cons':[([1,2],'≤',6),([2,1],'≤',8),([0,1],'≤',2)], 'signs':['x ≥ 0','x ≥ 0']}
OPS=['≤','≥','=']; OPMAP={'≤':'<=','≥':'>=','=':'='}; OPTEX={'<=':r'\leq','>=':r'\geq','=':'='}
SIGNS=['x ≥ 0','x ≤ 0','tự do']; SMAP={'x ≥ 0':'>=0','x ≤ 0':'<=0','tự do':'free'}

# ──────────────────── Sidebar (đã bỏ Nạp ví dụ + caption) ────────────────────
with st.sidebar:
    st.markdown('<div class="sb-greek">∑</div><div class="sb-brand">LP Solver</div>'
                '<div class="sb-desc">Quy hoạch tuyến tính · K23</div><hr>', unsafe_allow_html=True)
    st.markdown('<div class="sb-h">⑧ Quy tắc chọn biến vào</div>', unsafe_allow_html=True)
    rule_lbl = st.radio('rule', ['Mặc định — âm nhất (Dantzig)', 'Bland — chỉ số nhỏ nhất'],
                        label_visibility='collapsed')
    rule = 'bland' if 'Bland' in rule_lbl else 'dantzig'
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sb-h">Tùy chọn hiển thị</div>', unsafe_allow_html=True)
    show_dict = st.checkbox('Hiển thị các bước từ vựng', value=True)
    st.markdown('<hr><div class="sb-desc">Hỗ trợ: max / min · ràng buộc ≤ ≥ = · '
                'biến ≥0, ≤0, tự do · đơn hình 2 pha · quy tắc Bland · hình học (2 biến).</div>',
                unsafe_allow_html=True)

# ──────────────────── ① Kích thước & mục tiêu ────────────────────
with st.container(border=True):
    slabel('①', 'Kích thước &amp; mục tiêu')
    c1, c2, c3 = st.columns([1,1,1.4])
    with c1: n = st.number_input('Số biến n', 1, 20, value=2, key='n')
    with c2: m = st.number_input('Số ràng buộc m', 1, 30, value=3, key='m')
    with c3: sense = st.radio('Hướng tối ưu', ['max','min'], horizontal=True, key='sense')
n, m = int(n), int(m)

# ──────────────────── ② Hàm mục tiêu ────────────────────
with st.container(border=True):
    slabel('②', 'Hàm mục tiêu')
    obj=[]; cols=st.columns(n)
    for j in range(n):
        d = DEF['obj'][j] if j < len(DEF['obj']) else 0.0
        with cols[j]:
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#454b54">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
            obj.append(st.number_input(f'c{j+1}', value=float(d), step=1.0, key=f'o{j}', format='%g', label_visibility='collapsed'))

# ──────────────────── ③ Hệ ràng buộc ────────────────────
with st.container(border=True):
    slabel('③', 'Hệ ràng buộc')
    constraints=[]
    for i in range(m):
        cols=st.columns([*([1]*n), .7, 1.1]); row=[]
        for j in range(n):
            d = DEF['cons'][i][0][j] if (i < len(DEF['cons']) and j < len(DEF['cons'][i][0])) else 0.0
            with cols[j]: row.append(st.number_input(f'a{i}{j}', value=float(d), step=1.0, key=f'a{i}{j}', format='%g', label_visibility='collapsed'))
        with cols[n]:
            dop = DEF['cons'][i][1] if i < len(DEF['cons']) else '≤'
            op = st.selectbox(f'op{i}', OPS, index=OPS.index(dop), key=f'op{i}', label_visibility='collapsed')
        with cols[n+1]:
            db = DEF['cons'][i][2] if i < len(DEF['cons']) else 0.0
            rhs = st.number_input(f'b{i}', value=float(db), step=1.0, key=f'b{i}', format='%g', label_visibility='collapsed')
        constraints.append((row, OPMAP[op], rhs))

# ──────────────────── ④ Dấu biến ────────────────────
with st.container(border=True):
    slabel('④', 'Điều kiện dấu của biến')
    signs=[]; cols=st.columns(n)
    for j in range(n):
        ds = DEF['signs'][j] if j < len(DEF['signs']) else 'x ≥ 0'
        with cols[j]:
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#454b54">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
            signs.append(SMAP[st.selectbox(f's{j}', SIGNS, index=SIGNS.index(ds), key=f's{j}', label_visibility='collapsed')])

# ──────────────────── Xem trước ────────────────────
with st.container(border=True):
    slabel('≡', 'Xem trước bài toán')
    op_lines = [latex_expr(co) + " &" + OPTEX[op] + " " + fmt(F(b)) + r" \\" for (co,op,b) in constraints]
    sgn=[]
    for i,s in enumerate(signs):
        sgn.append(f"x_{{{i+1}}}\\geq 0" if s=='>=0' else (f"x_{{{i+1}}}\\leq 0" if s=='<=0' else f"x_{{{i+1}}}\\ \\text{{tự do}}"))
    st.latex(r"\%s\quad z = %s" % (sense, latex_expr(obj)))
    st.latex(r"\text{v.đk}\quad\begin{cases}" + "\n".join(op_lines) + r"\\ " + ",\\ ".join(sgn) + r"\end{cases}")

st.markdown('<br>', unsafe_allow_html=True)
col_b,_ = st.columns([1.2,4])
with col_b: go = st.button('GIẢI BÀI TOÁN', type='primary', use_container_width=True)

if go:
    try:
        res = solve(sense, [F(v) for v in obj],
                    [([F(x) for x in c], op, F(b)) for c,op,b in constraints], signs, rule)
    except Exception as e:
        st.error(f'Lỗi: {e}'); st.stop()

    st.markdown('<div class="rline"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:Source Serif 4,serif;font-weight:600">Kết quả</h2>', unsafe_allow_html=True)
    status = res['status']

    if status == 'optimal':
        st.markdown('<span class="pill p-opt">● Tối ưu (Optimal)</span>', unsafe_allow_html=True)
        st.markdown('<div style="height:.7rem"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1,1.6])
        with c1:
            st.markdown(f'<div class="rcard"><div class="zlb">Giá trị tối ưu z*</div>'
                        f'<div class="zv">{fmt(res["opt_value"])}</div></div>', unsafe_allow_html=True)
        with c2:
            th = "".join(f"<th>x{j+1}</th>" for j in range(len(res['x'])))
            td = "".join(f"<td>{fmt(v)}</td>" for v in res['x'])
            st.markdown(f'<div class="rcard"><div class="zlb">Nghiệm tối ưu</div>'
                        f'<table class="rtab"><thead><tr>{th}</tr></thead><tbody><tr>{td}</tr></tbody></table></div>', unsafe_allow_html=True)
        if res.get('multiple_optima'):
            st.info('ℹ️ Tồn tại biến phi cơ sở hệ số 0 → bài toán có thể có **vô số nghiệm tối ưu**.')
        if res.get('degenerate'):
            st.warning('⑧ **Suy biến** (có biến cơ sở = 0). Nếu cần đảm bảo không xoay vòng, chọn **Bland** ở thanh bên.')
    elif status == 'unbounded':
        st.markdown('<span class="pill p-unb">∞ Không giới nội (Unbounded)</span>', unsafe_allow_html=True)
    elif status == 'infeasible':
        st.markdown('<span class="pill p-inf">✕ Vô nghiệm (Infeasible)</span>', unsafe_allow_html=True)

    if n == 2 and status in ('optimal','unbounded','infeasible'):
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        slabel('④', 'Phương pháp hình học')
        try: st.pyplot(geo_draw(sense, obj, constraints, signs, res), use_container_width=True)
        except Exception as e: st.warning(f'Không vẽ được: {e}')

    with st.expander('Cách đặt biến phụ (đưa về dạng chuẩn)'):
        st.code(res.get('legend',''), language='text')

    if show_dict and res.get('steps'):
        st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)
        slabel('⑥', 'Các từ vựng từng bước')
        for k, stp in enumerate(res['steps'], 1):
            tag = ' · 🔸suy biến' if stp.get('degenerate_step') else ''
            with st.expander(f"Bước {k} · {stp['phase']}{tag} · vào {stp['enter']} · ra {stp['leave']}"):
                st.code(stp['dict_before'], language='text')
        if status == 'optimal':
            with st.expander('✓ Từ vựng cuối — NGHIỆM TỐI ƯU', expanded=True):
                st.code(res['final_dict'], language='text')

    st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
    slabel('↧', 'Xuất báo cáo LaTeX')
    tex = build_latex_document(sense, obj, constraints, signs, res, rule)
    st.download_button('⬇  Tải file .tex', data=tex.encode('utf-8'),
                       file_name='loi_giai_qhtt.tex', mime='text/plain', type='primary')
    with st.expander('Xem nội dung file .tex'):
        st.code(tex, language='latex')