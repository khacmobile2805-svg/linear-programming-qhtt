# -*- coding: utf-8 -*-
"""app.py — Giao diện web Streamlit (bản trau chuốt). Chạy: streamlit run app.py"""
import streamlit as st
from fractions import Fraction
from backend.core.solver import solve
from backend.core.geometry import draw as geo_draw
from backend.utils.formatting import fmt

st.set_page_config(page_title='Giải QHTT tổng quát', page_icon='📐', layout='wide')

# ─────────────────────────── GIAO DIỆN (CSS riêng) ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');
:root{
  --accent:#1f5f8b; --accent2:#2e8b87; --ink:#1a2230; --muted:#5b6776;
  --line:#e4e9f0; --bg:#f6f8fb; --card:#ffffff;
}
.stApp{ background:var(--bg); }
html, body, [class*="css"]{ font-family:'Inter',system-ui,sans-serif; color:var(--ink); }

/* Hero */
.hero{ background:linear-gradient(135deg,#1f5f8b 0%,#2e8b87 100%); color:#fff;
  padding:1.5rem 1.8rem; border-radius:16px; margin-bottom:1.4rem;
  box-shadow:0 6px 22px rgba(31,95,139,.20); }
.hero h1{ font-family:'Source Serif 4',Georgia,serif; font-size:1.65rem; line-height:1.25;
  margin:0 0 .35rem; font-weight:700; letter-spacing:.2px; }
.hero p{ margin:0; opacity:.93; font-size:.92rem; }
.hero .tags{ margin-top:.7rem; }
.hero .tag{ display:inline-block; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.25);
  padding:.18rem .6rem; border-radius:999px; font-size:.74rem; margin-right:.4rem; margin-top:.3rem; }

/* Section header */
.sec{ display:flex; align-items:center; gap:.65rem; margin:1.5rem 0 .7rem; }
.sec .n{ background:var(--accent); color:#fff; min-width:1.75rem; height:1.75rem; border-radius:9px;
  display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:.95rem; }
.sec h3{ margin:0; font-size:1.14rem; font-weight:600; }

/* Sidebar */
[data-testid="stSidebar"]{ background:#0f2233; }
[data-testid="stSidebar"] *{ color:#dce6f0 !important; }
[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{ color:#fff !important; }

/* Result card */
.zbox{ background:linear-gradient(135deg,#1f5f8b,#2e8b87); color:#fff; border-radius:14px;
  padding:1.1rem 1.3rem; box-shadow:0 4px 16px rgba(31,95,139,.18); }
.zbox .lbl{ font-size:.8rem; opacity:.9; text-transform:uppercase; letter-spacing:.5px; }
.zbox .val{ font-size:2rem; font-weight:700; font-family:'Source Serif 4',serif; }
.solbox{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:1.1rem 1.3rem; }
.solbox .lbl{ font-size:.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:.5px; margin-bottom:.4rem; }
.solbox .x{ display:inline-block; background:#eef4f9; color:var(--accent); font-weight:600;
  border-radius:8px; padding:.25rem .65rem; margin:.2rem .4rem .2rem 0; font-size:1.02rem; }

.stButton>button{ border-radius:10px; font-weight:600; }
hr{ border-color:var(--line); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Chương trình giải bài toán Quy hoạch tuyến tính tổng quát</h1>
  <p>Phương pháp đơn hình dạng từ vựng (2 pha) · tính bằng phân số chính xác</p>
  <div class="tags">
    <span class="tag">⑥ Đơn hình từ vựng</span>
    <span class="tag">⑧ Quy tắc Bland</span>
    <span class="tag">④ Hình học 2 biến</span>
    <span class="tag">Vô nghiệm · Không giới nội</span>
  </div>
</div>
""", unsafe_allow_html=True)

def sec(num, title):
    st.markdown(f'<div class="sec"><span class="n">{num}</span><h3>{title}</h3></div>',
                unsafe_allow_html=True)

def F(x): return Fraction(str(x))

EXAMPLES = {
    '— Tự nhập —': None,
    'VD ④⑥: max 3x₁+2x₂': {'sense':'max','n':2,'m':3,'obj':[3,2],'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([1,2],'≤',6),([2,1],'≤',8),([0,1],'≤',2)]},
    'VD ⑨ (vở): min 5x₁−7x₂': {'sense':'min','n':2,'m':3,'obj':[5,-7],'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([-4,1],'≤',-2),([1,1],'≤',5),([-1,-1],'≤',-1)]},
    'VD ⑧ Bland — suy biến': {'sense':'max','n':2,'m':4,'obj':[2,3],'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([2,1],'≤',14),([1,2],'≤',14),([1,1],'≤',8),([1,0],'≤',6)]},
    'VD vô nghiệm': {'sense':'max','n':2,'m':2,'obj':[1,1],'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([1,1],'≤',2),([1,1],'≥',5)]},
}
OPS=['≤','≥','=']; OPMAP={'≤':'<=','≥':'>=','=':'='}
SIGNS=['x ≥ 0','x ≤ 0','tự do']; SMAP={'x ≥ 0':'>=0','x ≤ 0':'<=0','tự do':'free'}

with st.sidebar:
    st.header('⚙ Thiết lập')
    pick = st.selectbox('Nạp ví dụ mẫu', list(EXAMPLES.keys()))
    if st.button('Nạp ví dụ') and EXAMPLES[pick]:
        ex = EXAMPLES[pick]
        st.session_state.update({'sense':ex['sense'],'n':ex['n'],'m':ex['m'],'_pre':ex})
    n = st.number_input('Số biến (n)', 1, 20, value=st.session_state.get('n',2), key='n')
    m = st.number_input('Số ràng buộc (m)', 1, 30, value=st.session_state.get('m',2), key='m')
    sense = st.radio('Mục tiêu', ['max','min'],
                     index=0 if st.session_state.get('sense','max')=='max' else 1,
                     horizontal=True, key='sense')
    st.divider()
    st.subheader('⑧ Quy tắc chọn biến vào')
    rule_lbl = st.radio('', ['Mặc định — hệ số âm nhất (Dantzig)',
                              'Bland — chỉ số nhỏ nhất (tránh xoay vòng)'], key='rule')
    rule = 'bland' if 'Bland' in rule_lbl else 'dantzig'
    st.caption('Dantzig khớp ví dụ vở. Bland dùng khi bài suy biến.')
    st.divider()
    show_geo  = st.checkbox('④ Vẽ miền nghiệm (khi n=2)', value=True)
    show_dict = st.checkbox('⑥ Hiển thị các từ vựng', value=True)

pre = st.session_state.get('_pre')

sec('1', 'Hàm mục tiêu')
obj=[]; cols=st.columns(n)
for j in range(n):
    d = pre['obj'][j] if (pre and j<len(pre['obj'])) else 0.0
    with cols[j]: obj.append(st.number_input(f'c{j+1} (x{j+1})',value=float(d),step=1.0,key=f'o{j}',format='%g'))

sec('2', 'Hệ ràng buộc')
constraints=[]
for i in range(m):
    cols=st.columns(n+2); row=[]
    for j in range(n):
        d = pre['cons'][i][0][j] if (pre and i<len(pre['cons'])) else 0.0
        with cols[j]: row.append(st.number_input(f'RB{i+1}·x{j+1}',value=float(d),step=1.0,key=f'a{i}{j}',format='%g'))
    with cols[n]:
        dop = pre['cons'][i][1] if (pre and i<len(pre['cons'])) else '≤'
        op = st.selectbox('Dấu',OPS,index=OPS.index(dop),key=f'op{i}')
    with cols[n+1]:
        db = pre['cons'][i][2] if (pre and i<len(pre['cons'])) else 0.0
        rhs = st.number_input('Vế phải',value=float(db),step=1.0,key=f'b{i}',format='%g')
    constraints.append((row,OPMAP[op],rhs))

sec('3', 'Điều kiện dấu của biến')
signs=[]; cols=st.columns(n)
for j in range(n):
    ds = pre['signs'][j] if (pre and j<len(pre['signs'])) else 'x ≥ 0'
    with cols[j]: signs.append(SMAP[st.selectbox(f'x{j+1}',SIGNS,index=SIGNS.index(ds),key=f's{j}')])

st.markdown('<br>', unsafe_allow_html=True)
if st.button('🚀  GIẢI BÀI TOÁN', type='primary', use_container_width=True):
    try:
        res = solve(sense, [F(v) for v in obj],
                    [([F(x) for x in c], op, F(b)) for c,op,b in constraints], signs, rule)
    except Exception as e:
        st.error(f'Lỗi: {e}'); st.stop()

    sec('📊', 'Kết quả')
    status = res['status']
    if status == 'optimal':
        c1,c2 = st.columns([1,2])
        with c1:
            st.markdown(f'<div class="zbox"><div class="lbl">Giá trị tối ưu z*</div>'
                        f'<div class="val">{fmt(res["opt_value"])}</div></div>', unsafe_allow_html=True)
        with c2:
            xs = ''.join(f'<span class="x">x{j+1} = {fmt(v)}</span>' for j,v in enumerate(res['x']))
            st.markdown(f'<div class="solbox"><div class="lbl">Nghiệm tối ưu</div>{xs}</div>',
                        unsafe_allow_html=True)
        if res.get('multiple_optima'):
            st.info('ℹ️ Có thể có **vô số nghiệm tối ưu** (biến phi cơ sở hệ số 0).')
        if res.get('degenerate'):
            st.warning('⑧ **Suy biến:** có biến cơ sở = 0. Nếu cần, chọn quy tắc **Bland** ở thanh bên.')
    elif status == 'unbounded':
        st.warning('⚠️ Bài toán **KHÔNG BỊ CHẶN** (hàm mục tiêu → ±∞).')
    elif status == 'infeasible':
        st.error('❌ Bài toán **VÔ NGHIỆM** (miền ràng buộc rỗng).')

    if show_geo and int(n)==2 and status in ('optimal','unbounded','infeasible'):
        sec('④', 'Phương pháp hình học')
        try:
            st.pyplot(geo_draw(sense, obj, constraints, signs, res), use_container_width=True)
        except Exception as e:
            st.warning(f'Không vẽ được: {e}')

    with st.expander('ℹ️ Cách đặt biến phụ (đưa về dạng chuẩn)'):
        st.code(res.get('legend',''), language='text')

    if show_dict and res.get('steps'):
        sec('⑥', 'Các từ vựng từng bước')
        for k,stp in enumerate(res['steps'],1):
            tag = ' 🔸suy biến' if stp.get('degenerate_step') else ''
            with st.expander(f"Bước {k} · {stp['phase']}{tag} · vào: {stp['enter']} · ra: {stp['leave']}"):
                st.code(stp['dict_before'], language='text')
        if status=='optimal':
            with st.expander('✅ Từ vựng cuối — NGHIỆM TỐI ƯU', expanded=True):
                st.code(res['final_dict'], language='text')
