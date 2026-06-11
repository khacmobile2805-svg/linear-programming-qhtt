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
  --ink:#1c2230; --ink2:#4a5160; --ink3:#8a93a3;
  --bg-top: #f4f7f9;
  --bg-bottom: #eaf0f6;
  --panel: #ffffff;
  --line: #e2e8f0;
  --line2: #f1f5f9;
  --field: #f8fafc;
  --field-bd: #cbd5e1;
  --field-tx: #0f172a;
  --accent:#1d4ed8; --accent2:#1e40af; --accent-soft:#eff6ff;
  --green:#166534; --green-lt:#dcfce7; --red:#991b1b; --red-lt:#fee2e2;
  --amber:#92400e; --amber-lt:#fef3c7;
}
[data-testid="stAppViewContainer"]{
    background: linear-gradient(160deg, var(--bg-top) 0%, var(--bg-bottom) 100%) !important;
}
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stMainBlockContainer"]{ max-width:1100px; padding-top:2.8rem; }
html, body, [class*="css"]{ font-family:'Inter',system-ui,sans-serif; color:var(--ink); }
.mast{
  background: linear-gradient(135deg, #1e2d4a 0%, #1d4ed8 100%);
  border-radius:14px; text-align:center;
  padding:1.45rem 1.6rem; margin-bottom:1.9rem;
  box-shadow:0 8px 24px rgba(29,78,216,.20);
}
.mast .t{ font-family:'Agbalumo','Source Serif 4',serif; font-weight:400; color:#ffffff;
  font-size:clamp(.85rem,1.75vw,1.4rem); line-height:1.5; text-transform:uppercase; white-space:nowrap; margin:0;
  text-shadow:0 1px 2px rgba(0,0,0,.15); }
.mast .s{ font-size:.72rem; letter-spacing:.16em; text-transform:uppercase; color:rgba(255,255,255,.80); margin-top:.5rem; }
.slabel{ display:flex; align-items:center; gap:.55rem; font-size:.7rem; font-weight:600;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink3); margin:0 0 .8rem; }
.slabel .n{ display:inline-flex; align-items:center; justify-content:center; width:20px;height:20px;
  border-radius:50%; background:var(--accent-soft); color:var(--accent); font-size:.66rem; font-weight:700; }
[data-testid="stVerticalBlockBorderWrapper"]{
  background:var(--panel) !important;
  border-color:var(--line) !important;
  border-radius:12px !important;
  box-shadow:0 2px 8px rgba(15,23,42,.05);
  transition:box-shadow .2s ease, border-color .2s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover{
  box-shadow:0 8px 24px rgba(29,78,216,.10);
  border-color:#bfdbfe !important;
}
[data-testid="stNumberInput"] input{
  background:var(--field) !important; color:var(--field-tx) !important;
  -webkit-text-fill-color: var(--field-tx) !important;
  border:1px solid var(--field-bd) !important; border-radius:8px !important;
  font-family:'JetBrains Mono',monospace !important; text-align:center !important;
  transition:border-color .15s, box-shadow .15s;
}
[data-testid="stNumberInput"] input:focus{
  border-color:var(--accent) !important;
  background:#ffffff !important;
  box-shadow:0 0 0 3px var(--accent-soft) !important;
}
[data-testid="stNumberInput"] button{
  background:var(--field) !important; color:var(--ink2) !important; border-color:var(--field-bd) !important;
}
[data-testid="stNumberInput"] button:hover{ background:#e2e8f0 !important; }
[data-testid="stTextInput"] input{
  background:var(--field) !important; color:var(--field-tx) !important;
  -webkit-text-fill-color: var(--field-tx) !important;
  border:1px solid var(--field-bd) !important; border-radius:8px !important;
  font-family:'JetBrains Mono',monospace !important; text-align:center !important;
  transition:border-color .15s, box-shadow .15s;
}
[data-testid="stTextInput"] input:focus{
  border-color:var(--accent) !important; background:#ffffff !important;
  box-shadow:0 0 0 3px var(--accent-soft) !important;
}
[data-baseweb="select"]>div{
  background:var(--field) !important; border:1px solid var(--field-bd) !important;
  border-radius:8px !important; transition:border-color .15s, box-shadow .15s;
}
[data-baseweb="select"]>div:focus-within{
  border-color:var(--accent) !important; background:#ffffff !important;
  box-shadow:0 0 0 3px var(--accent-soft) !important;
}
[data-baseweb="select"] div, [data-baseweb="select"] span{
  color:var(--field-tx) !important; -webkit-text-fill-color: var(--field-tx) !important;
  font-family:'JetBrains Mono',monospace !important;
}
[data-baseweb="select"] svg{ fill:var(--ink3) !important; }
ul[role="listbox"]{
  background:#ffffff !important; border:1px solid var(--line) !important;
  border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,.10) !important;
}
li[role="option"]{ color:var(--ink) !important; background:#ffffff !important; }
li[role="option"]:hover{ background:var(--accent-soft) !important; color:var(--accent) !important; }
[data-testid="stSidebar"]{ background:#1e2d4a !important; border-right:1px solid #162238; }
[data-testid="stSidebar"] *{ color:#8a93a3 !important; }
[data-testid="stSidebar"] hr{ border-color:#2a3f5f !important; }
.sb-brand{ font-family:'Source Serif 4',serif; font-size:1.15rem; color:#e2e8f0 !important; line-height:1.25; font-weight:600; }
.sb-desc{ font-size:.72rem; color:#64748b !important; letter-spacing:.03em; }
.sb-h{ font-size:.68rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; color:#64748b !important; margin:.2rem 0 .4rem;}
[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label p{ color:#cbd5e1 !important; }
.rline{ border-top:1px solid var(--line); margin:2rem 0 1.3rem; }
.pill{ display:inline-flex; align-items:center; gap:.4rem; font-size:.74rem; font-weight:600;
  letter-spacing:.07em; text-transform:uppercase; padding:5px 13px; border-radius:100px; }
.p-opt{ background:var(--green-lt); color:var(--green);}
.p-inf{ background:var(--red-lt); color:var(--red);}
.p-unb{ background:var(--amber-lt); color:var(--amber);}
.rcard{
  background:var(--panel);
  border:1px solid var(--line); border-radius:12px; padding:1.1rem 1.3rem;
  box-shadow:0 2px 8px rgba(15,23,42,.04);
}
.rcard .zlb{ font-size:.68rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--ink3);}
.rcard .zv{ font-family:'Source Serif 4',serif; font-size:1.85rem; font-weight:700; color:var(--accent); }
.rtab{ width:100%; border-collapse:collapse; font-family:'JetBrains Mono',monospace; font-size:.92rem; margin-top:.3rem;}
.rtab th{ border-bottom:1.5px solid var(--line); padding:6px 14px; color:var(--ink2); background:var(--field);}
.rtab td{ border-bottom:1px solid var(--line2); padding:7px 14px; text-align:center; color:var(--ink);}
div.stButton>button[kind="primary"]{
  background:var(--accent) !important;
  border:none !important; color:#ffffff !important;
  border-radius:9px !important; font-weight:600 !important; letter-spacing:.02em !important;
  transition:background .18s, transform .1s, box-shadow .1s !important;
}
div.stButton>button[kind="primary"]:hover{
  background:var(--accent2) !important;
  box-shadow:0 4px 12px rgba(29,78,216,.3) !important;
}
div.stButton>button[kind="primary"]:active{ transform:translateY(1px) !important; box-shadow:none !important; }
[data-testid="stExpander"]{
  border:1px solid var(--line) !important; border-radius:10px !important;
  background:var(--panel) !important; box-shadow:0 2px 8px rgba(15,23,42,.02) !important;
}
h1,h2,h3,h4{ color:var(--ink) !important; }
hr{ border-color:var(--line); }
p, label, .stMarkdown{ color:var(--ink) !important; }
[data-testid="stInfo"]{ background:#eff6ff !important; border-color:#bfdbfe !important; color:#1e40af !important; }
[data-testid="stWarning"]{ background:var(--amber-lt) !important; border-color:#fde68a !important; color:var(--amber) !important; }
[data-testid="stError"]{ background:var(--red-lt) !important; border-color:#fecaca !important; color:var(--red) !important; }
[data-testid="stCode"], .stCode{ background:#f8fafc !important; border:1px solid var(--line) !important; color:#334155 !important; }
code{ color:#1d4ed8 !important; }
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

def pf(t):
    """Đọc hệ số: số nguyên (3), thập phân (0.5) hoặc phân số (1/3)."""
    t = (t or '').strip().replace(' ', '')
    return Fraction(0) if t == '' else Fraction(t)

DEF = {'obj':[3,2], 'cons':[([1,2],'≤',6),([2,1],'≤',8),([0,1],'≤',2)], 'signs':['x ≥ 0','x ≥ 0']}
OPS=['≤','≥','=']; OPMAP={'≤':'<=','≥':'>=','=':'='}; OPTEX={'<=':r'\leq','>=':r'\geq','=':'='}
SIGNS=['x ≥ 0','x ≤ 0','tự do']; SMAP={'x ≥ 0':'>=0','x ≤ 0':'<=0','tự do':'free'}

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

with st.container(border=True):
    slabel('①', 'Kích thước &amp; mục tiêu')
    c1, c2, c3 = st.columns([1,1,1.4])
    with c1: n = st.number_input('Số biến n', 1, 20, value=2, key='n', help='Số biến quyết định: x₁, x₂, …')
    with c2: m = st.number_input('Số ràng buộc m', 1, 30, value=3, key='m', help='Số ràng buộc, chưa kể điều kiện dấu')
    with c3: sense = st.radio('Hướng tối ưu', ['max','min'], horizontal=True, key='sense')
n, m = int(n), int(m)

with st.container(border=True):
    slabel('②', 'Hàm mục tiêu')
    obj_raw=[]; cols=st.columns(n)
    for j in range(n):
        d = str(DEF['obj'][j]) if j < len(DEF['obj']) else '0'
        with cols[j]:
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#8a93a3">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
            obj_raw.append(st.text_input(f'c{j+1}', value=d, key=f'o{j}', label_visibility='collapsed'))

with st.container(border=True):
    slabel('③', 'Hệ ràng buộc')
    cons_raw=[]
    for i in range(m):
        cols=st.columns([*([1]*n), .7, 1.1]); row=[]
        for j in range(n):
            d = str(DEF['cons'][i][0][j]) if (i < len(DEF['cons']) and j < len(DEF['cons'][i][0])) else '0'
            with cols[j]: row.append(st.text_input(f'a{i}{j}', value=d, key=f'a{i}{j}', label_visibility='collapsed'))
        with cols[n]:
            dop = DEF['cons'][i][1] if i < len(DEF['cons']) else '≤'
            op = st.selectbox(f'op{i}', OPS, index=OPS.index(dop), key=f'op{i}', label_visibility='collapsed')
        with cols[n+1]:
            db = str(DEF['cons'][i][2]) if i < len(DEF['cons']) else '0'
            rhs = st.text_input(f'b{i}', value=db, key=f'b{i}', label_visibility='collapsed')
        cons_raw.append((row, OPMAP[op], rhs))

with st.container(border=True):
    slabel('④', 'Điều kiện dấu của biến')
    signs=[]; cols=st.columns(n)
    for j in range(n):
        ds = DEF['signs'][j] if j < len(DEF['signs']) else 'x ≥ 0'
        with cols[j]:
            st.markdown(f'<div style="text-align:center;font-family:JetBrains Mono;color:#8a93a3">x<sub>{j+1}</sub></div>', unsafe_allow_html=True)
            signs.append(SMAP[st.selectbox(f's{j}', SIGNS, index=SIGNS.index(ds), key=f's{j}', label_visibility='collapsed')])

# ── Đọc & kiểm tra hệ số (hỗ trợ phân số 1/3) ──
parse_ok = True; obj_f = []; cons_f = []
try:
    obj_f = [pf(v) for v in obj_raw]
    for (row, op, rb) in cons_raw:
        cons_f.append(([pf(x) for x in row], op, pf(rb)))
except (ValueError, ZeroDivisionError):
    parse_ok = False

with st.container(border=True):
    slabel('≡', 'Xem trước bài toán')
    st.caption('Mẹo: hệ số có thể nhập phân số (vd 1/3, -2/5), thập phân (0.5) hoặc số nguyên.')
    if not parse_ok:
        st.warning('Có hệ số nhập chưa hợp lệ — chỉ dùng số nguyên, thập phân hoặc phân số dạng a/b.')
    else:
        op_lines = [latex_expr(co) + " &" + OPTEX[op] + " " + fmt(b) + r" \\" for (co,op,b) in cons_f]
        sgn=[]
        for i,s in enumerate(signs):
            sgn.append(f"x_{{{i+1}}}\\geq 0" if s=='>=0' else (f"x_{{{i+1}}}\\leq 0" if s=='<=0' else f"x_{{{i+1}}}\\ \\text{{tự do}}"))
        st.latex(r"\%s\quad z = %s" % (sense, latex_expr(obj_f)))
        st.latex(r"\text{v.đk}\quad\begin{cases}" + "\n".join(op_lines) + r"\\ " + ",\\ ".join(sgn) + r"\end{cases}")

st.markdown('<br>', unsafe_allow_html=True)
col_b,_ = st.columns([1.2,4])
with col_b: go = st.button('GIẢI BÀI TOÁN', type='primary', use_container_width=True)

if go:
    if not parse_ok:
        st.error('Có hệ số nhập sai định dạng. Chỉ chấp nhận số nguyên (3), thập phân (0.5) hoặc phân số (1/3).'); st.stop()
    try:
        res = solve(sense, obj_f, cons_f, signs, rule)
    except Exception as e:
        st.error(f'Lỗi: {e}'); st.stop()

    st.markdown('<div class="rline"></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:Source Serif 4,serif;font-weight:600;color:#1c2230">Kết quả</h2>', unsafe_allow_html=True)
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

        # ── Kiểm chứng nghiệm: thay vào ràng buộc gốc ──
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        with st.expander('✓ Kiểm chứng nghiệm (thay vào ràng buộc gốc)', expanded=False):
            OPV = {'<=':'≤','>=':'≥','=':'='}
            rows = ''
            for i, c in enumerate(res['checks'], 1):
                mark = '✓' if c['ok'] else '✗'
                rows += (f"<tr><td>RB {i}</td><td>{fmt(c['lhs'])}</td>"
                         f"<td>{OPV[c['op']]}</td><td>{fmt(c['rhs'])}</td><td>{mark}</td></tr>")
            st.markdown(
                f'<table class="rtab"><thead><tr><th>Ràng buộc</th><th>Vế trái</th>'
                f'<th>Dấu</th><th>Vế phải</th><th>Đạt</th></tr></thead><tbody>{rows}</tbody></table>',
                unsafe_allow_html=True)
            st.markdown(f'<div style="margin-top:.7rem;font-family:JetBrains Mono">'
                        f'z tính lại từ nghiệm = <b>{fmt(res["z_check"])}</b></div>', unsafe_allow_html=True)
            if res['all_ok']:
                st.success('Nghiệm thỏa mãn TẤT CẢ ràng buộc gốc — kết quả được kiểm chứng đúng.')
            else:
                st.error('Có ràng buộc chưa thỏa — vui lòng kiểm tra lại dữ liệu nhập.')
    elif status == 'unbounded':
        st.markdown('<span class="pill p-unb">∞ Không giới nội (Unbounded)</span>', unsafe_allow_html=True)
    elif status == 'infeasible':
        st.markdown('<span class="pill p-inf">✕ Vô nghiệm (Infeasible)</span>', unsafe_allow_html=True)
    elif status == 'cycling':
        st.markdown('<span class="pill p-unb">↻ Nghi xoay vòng (Cycling)</span>', unsafe_allow_html=True)
        st.warning('Bài toán suy biến khiến quy tắc Dantzig xoay vòng quá nhiều bước. '
                   'Hãy chọn **Bland — chỉ số nhỏ nhất** ở thanh bên rồi giải lại (Bland đảm bảo dừng).')

    if n == 2 and status in ('optimal','unbounded','infeasible'):
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        slabel('④', 'Phương pháp hình học')
        try: st.pyplot(geo_draw(sense, obj_f, cons_f, signs, res), use_container_width=True)
        except Exception as e: st.warning(f'Không vẽ được: {e}')

    with st.expander('Cách đặt biến phụ (đưa về dạng chuẩn)'):
        st.code(res.get('legend',''), language='text')

    if res.get('standard_form'):
        with st.expander('Dạng chuẩn — bài toán min tương đương'):
            st.code(res['standard_form'], language='text')

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