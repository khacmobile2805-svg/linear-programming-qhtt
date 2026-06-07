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
  --ink:#e2e8f0; --ink2:#94a3b8; --ink3:#64748b;

  /* NAVY & ORANGE — tông tối sang trọng */
  --bg-top: #0f172a;
  --bg-bottom: #1e3a5f;
  --panel: #1a2744;
  --line: #2a3f5f;
  --line2: #1e2f4a;

  /* Ô nhập liệu: tối, viền navy nhạt, chữ sáng */
  --field: #0f1f38;
  --field-bd: #2a3f5f;
  --field-tx: #e2e8f0;

  /* Accent chính: Cam nổi bật */
  --accent:#ea580c; --accent2:#c2410c; --accent-soft:rgba(234,88,12,.15);

  /* Trạng thái kết quả */
  --green:#86efac; --green-lt:rgba(134,239,172,.12); --red:#fca5a5; --red-lt:rgba(252,165,165,.12);
  --amber:#fcd34d; --amber-lt:rgba(252,211,77,.12);
}

/* Nền gradient navy */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg, var(--bg-top) 0%, var(--bg-bottom) 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stMainBlockContainer"]{ max-width:1100px; padding-top:2.8rem; }
html, body, [class*="css"]{ font-family:'Inter',system-ui,sans-serif; color:var(--ink); }

/* Tiêu đề — gradient cam đậm */
.mast{
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #7c2d12 100%);
  border: 1px solid rgba(234,88,12,.4);
  border-radius:14px; text-align:center;
  padding:1.45rem 1.6rem; margin-bottom:1.9rem;
  box-shadow:0 8px 32px rgba(234,88,12,.25), 0 0 0 1px rgba(234,88,12,.1);
}
.mast .t{ font-family:'Agbalumo','Source Serif 4',serif; font-weight:400; color:#fed7aa;
  font-size:clamp(.85rem,1.75vw,1.4rem); line-height:1.5; text-transform:uppercase; white-space:nowrap; margin:0;
  text-shadow:0 1px 4px rgba(234,88,12,.4); }
.mast .s{ font-size:.72rem; letter-spacing:.16em; text-transform:uppercase; color:rgba(253,186,116,.75); margin-top:.5rem; }

.slabel{ display:flex; align-items:center; gap:.55rem; font-size:.7rem; font-weight:600;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink3); margin:0 0 .8rem; }
.slabel .n{ display:inline-flex; align-items:center; justify-content:center; width:20px;height:20px;
  border-radius:50%; background:var(--accent-soft); color:var(--accent); font-size:.66rem; font-weight:700; border:1px solid rgba(234,88,12,.3); }

/* Panel cards — nền navy panel */
[data-testid="stVerticalBlockBorderWrapper"]{
  background:var(--panel) !important;
  border-color:var(--line) !important;
  border-radius:12px !important;
  box-shadow:0 2px 12px rgba(0,0,0,.3);
  transition:box-shadow .2s ease, border-color .2s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover{
  box-shadow:0 8px 28px rgba(234,88,12,.15);
  border-color:rgba(234,88,12,.35) !important;
}

/* Ô nhập liệu */
[data-testid="stNumberInput"] input{
  background:var(--field) !important; color:var(--field-tx) !important;
  -webkit-text-fill-color: var(--field-tx) !important;
  border:1px solid var(--field-bd) !important; border-radius:8px !important;
  font-family:'JetBrains Mono',monospace !important; text-align:center !important;
  transition:border-color .15s, box-shadow .15s;
}
[data-testid="stNumberInput"] input:focus{
  border-color:var(--accent) !important;
  background:#0a1628 !important;
  box-shadow:0 0 0 3px var(--accent-soft) !important;
}
[data-testid="stNumberInput"] button{
  background:var(--field) !important; color:var(--ink2) !important; border-color:var(--field-bd) !important;
}
[data-testid="stNumberInput"] button:hover{ background:#1e2f4a !important; color:var(--accent) !important; }

[data-baseweb="select"]>div{
  background:var(--field) !important; border:1px solid var(--field-bd) !important;
  border-radius:8px !important; transition:border-color .15s, box-shadow .15s;
}
[data-baseweb="select"]>div:focus-within{
  border-color:var(--accent) !important; background:#0a1628 !important;
  box-shadow:0 0 0 3px var(--accent-soft) !important;
}
[data-baseweb="select"] div, [data-baseweb="select"] span{
  color:var(--field-tx) !important; -webkit-text-fill-color: var(--field-tx) !important;
  font-family:'JetBrains Mono',monospace !important;
}
[data-baseweb="select"] svg{ fill:var(--ink2) !important; }
ul[role="listbox"]{
  background:#1a2744 !important; border:1px solid var(--line) !important;
  border-radius:8px; box-shadow:0 8px 24px rgba(0,0,0,.5) !important;
}
li[role="option"]{ color:var(--ink) !important; background:#1a2744 !important; }
li[role="option"]:hover{ background:var(--accent-soft) !important; color:#fed7aa !important; }

/* Sidebar */
[data-testid="stSidebar"]{ background:#0d1b2e !important; border-right:1px solid var(--line); }
[data-testid="stSidebar"] *{ color:var(--ink2) !important; }
[data-testid="stSidebar"] .sb-brand{ color:#fed7aa !important; }
.sb-brand{ font-family:'Source Serif 4',serif; font-size:1.15rem; color:#fed7aa !important; line-height:1.25; font-weight:600; }
.sb-desc{ font-size:.72rem; color:var(--ink3) !important; letter-spacing:.03em; }
.sb-h{ font-size:.68rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; color:var(--accent) !important; margin:.2rem 0 .4rem;}

/* Radio & checkbox trong sidebar */
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label{ color:var(--ink) !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] p,
[data-testid="stSidebar"] [data-testid="stCheckbox"] p{ color:var(--ink2) !important; }

.rline{ border-top:1px solid var(--line); margin:2rem 0 1.3rem; }

/* Pills kết quả */
.pill{ display:inline-flex; align-items:center; gap:.4rem; font-size:.74rem; font-weight:600;
  letter-spacing:.07em; text-transform:uppercase; padding:5px 13px; border-radius:100px; }
.p-opt{ background:rgba(134,239,172,.12); color:var(--green); border:1px solid rgba(134,239,172,.25);}
.p-inf{ background:rgba(252,165,165,.12); color:var(--red); border:1px solid rgba(252,165,165,.25);}
.p-unb{ background:rgba(252,211,77,.12); color:var(--amber); border:1px solid rgba(252,211,77,.25);}

/* Card kết quả */
.rcard{
  background:linear-gradient(135deg, #0f1f38 0%, #1a2744 100%);
  border:1px solid var(--line); border-radius:12px; padding:1.1rem 1.3rem;
  box-shadow:0 2px 12px rgba(0,0,0,.3);
}
.rcard .zlb{ font-size:.68rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--ink3);}
.rcard .zv{ font-family:'Source Serif 4',serif; font-size:1.85rem; font-weight:700; color:var(--accent); text-shadow:0 0 20px rgba(234,88,12,.4); }

/* Bảng kết quả */
.rtab{ width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:.92rem; margin-top:.3rem;}
.rtab th{ border-bottom:1.5px solid var(--line); padding:6px 14px; color:var(--ink2); background:#0f1f38;}
.rtab td{ border-bottom:1px solid var(--line2); padding:7px 14px; text-align:center; color:var(--ink);}

/* Nút GIẢI BÀI TOÁN — cam nổi bật */
div.stButton>button[kind="primary"]{
  background:linear-gradient(135deg, #ea580c, #c2410c) !important;
  border:none !important; color:#ffffff !important;
  border-radius:9px !important; font-weight:600 !important; letter-spacing:.06em !important;
  box-shadow:0 4px 16px rgba(234,88,12,.4) !important;
  transition:all .18s !important;
}
div.stButton>button[kind="primary"]:hover{
  background:linear-gradient(135deg, #f97316, #ea580c) !important;
  box-shadow:0 6px 24px rgba(234,88,12,.6) !important;
  transform:translateY(-1px) !important;
}
div.stButton>button[kind="primary"]:active{ transform:translateY(1px) !important; box-shadow:none !important; }

/* Expander */
[data-testid="stExpander"]{
  border:1px solid var(--line) !important; border-radius:10px !important;
  background:var(--panel) !important; box-shadow:0 2px 8px rgba(0,0,0,.2) !important;
}
[data-testid="stExpander"] summary:hover{ border-color:rgba(234,88,12,.35) !important; }

/* Headings và text */
h1,h2,h3,h4{ color:var(--ink) !important; }
hr{ border-color:var(--line); }
p, label, .stMarkdown{ color:var(--ink) !important; }

/* Info/warning/error messages */
[data-testid="stInfo"]{ background:rgba(234,88,12,.1) !important; border-color:rgba(234,88,12,.35) !important; color:#fed7aa !important; }
[data-testid="stWarning"]{ background:rgba(252,211,77,.1) !important; border-color:rgba(252,211,77,.3) !important; color:var(--amber) !important; }
[data-testid="stError"]{ background:rgba(252,165,165,.1) !important; border-color:rgba(252,165,165,.25) !important; color:var(--red) !important; }

/* Code blocks */
[data-testid="stCode"], .stCode{ background:#050d1a !important; border:1px solid var(--line) !important; color:#7dd3fc !important; }
code{ color:#fbd38d !important; }
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

DEF = {'obj':[3,2], 'cons':[([1,2],'≤',6),([2,1],'≤',8),([0,1],'≤',2)], 'signs':['x ≥ 0','x ≥ 0']}
OPS=['≤','≥','=']; OPMAP={'≤':'<=','≥':'>=','=':'='}; OPTEX={'<=':r'\leq','>=':r'\geq','=':'='}
SIGNS=['x ≥ 0','x ≤ 0','tự do']; SMAP={'x ≥ 0':'>=0','x ≤ 0':'<=0','tự do':'free'}

# ──────────────────── Sidebar ────────────────────
with st.sidebar:
    st.markdown('<div class="sb-brand">Linear Programming Solver</div>'
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
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#94a3b8">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
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
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#94a3b8">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
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
    st.markdown('<h2 style="font-family:Source Serif 4,serif;font-weight:600;color:#e2e8f0">Kết quả</h2>', unsafe_allow_html=True)
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