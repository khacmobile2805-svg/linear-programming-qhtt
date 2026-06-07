# -*- coding: utf-8 -*-
"""
app.py — Giao diện web Streamlit
Chạy:  streamlit run app.py
Bao gồm: ④ Hình học (2 biến), ⑥ Đơn hình từ vựng, ⑧ Bland / suy biến
"""
import streamlit as st
from fractions import Fraction

from backend.core.solver import solve
from backend.core.geometry import draw as geo_draw
from backend.utils.formatting import fmt

# ─── Cấu hình trang ────────────────────────────────────────────────────
st.set_page_config(page_title='Giải QHTT tổng quát', page_icon='📐', layout='wide')
st.title('📐 Chương trình giải bài toán Quy hoạch tuyến tính tổng quát')
st.caption('⑥ Đơn hình từ vựng · ⑧ Quy tắc Bland · ④ Hình học (2 biến) · Phân số chính xác')

def F(x): return Fraction(str(x))

# ─── Ví dụ mẫu ─────────────────────────────────────────────────────────
EXAMPLES = {
    '— Tự nhập —': None,
    'VD vở ④⑥: max 3x₁+2x₂': {
        'sense':'max','n':2,'m':3,'obj':[3,2],
        'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([1,2],'≤',6),([2,1],'≤',8),([0,1],'≤',2)]},
    'VD vở ⑨: min 5x₁−7x₂ (2 pha)': {
        'sense':'min','n':2,'m':3,'obj':[5,-7],
        'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([-4,1],'≤',-2),([1,1],'≤',5),([-1,-1],'≤',-1)]},
    'VD ⑧ suy biến (Bland): max 2x₁+3x₂': {
        'sense':'max','n':2,'m':4,'obj':[2,3],
        'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([2,1],'≤',14),([1,2],'≤',14),([1,1],'≤',8),([1,0],'≤',6)]},
    'VD vô nghiệm': {
        'sense':'max','n':2,'m':2,'obj':[1,1],
        'signs':['x ≥ 0','x ≥ 0'],
        'cons':[([1,1],'≤',2),([1,1],'≥',5)]},
}

OPS   = ['≤','≥','=']; OPMAP = {'≤':'<=','≥':'>=','=':'='}
SIGNS = ['x ≥ 0','x ≤ 0','tự do']
SMAP  = {'x ≥ 0':'>=0','x ≤ 0':'<=0','tự do':'free'}

# ─── Sidebar ───────────────────────────────────────────────────────────
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
    rule_lbl = st.radio('',
        ['Mặc định — hệ số âm nhất (Dantzig)',
         'Bland — chỉ số nhỏ nhất (tránh xoay vòng)'], key='rule')
    rule = 'bland' if 'Bland' in rule_lbl else 'dantzig'
    st.caption('Dantzig khớp ví dụ vở. Bland dùng khi bài suy biến.')
    st.divider()
    show_geo  = st.checkbox('④ Vẽ miền nghiệm (chỉ khi n=2)', value=True)
    show_dict = st.checkbox('⑥ Hiển thị các từ vựng', value=True)
    st.markdown('---\n*Hệ số nhập: số âm, thập phân.*')

pre = st.session_state.get('_pre')

# ─── 1. Hàm mục tiêu ───────────────────────────────────────────────────
st.subheader('1️⃣ Hàm mục tiêu')
obj = []
cols = st.columns(n)
for j in range(n):
    d = pre['obj'][j] if (pre and j<len(pre['obj'])) else 0.0
    with cols[j]:
        obj.append(st.number_input(f'c{j+1} (x{j+1})', value=float(d),
                                   step=1.0, key=f'o{j}', format='%g'))

# ─── 2. Ràng buộc ──────────────────────────────────────────────────────
st.subheader('2️⃣ Hệ ràng buộc')
constraints = []
for i in range(m):
    cols = st.columns(n+2); row=[]
    for j in range(n):
        d = pre['cons'][i][0][j] if (pre and i<len(pre['cons'])) else 0.0
        with cols[j]:
            row.append(st.number_input(f'RB{i+1}·x{j+1}', value=float(d),
                                       step=1.0, key=f'a{i}{j}', format='%g'))
    with cols[n]:
        dop = pre['cons'][i][1] if (pre and i<len(pre['cons'])) else '≤'
        op  = st.selectbox('', OPS, index=OPS.index(dop), key=f'op{i}')
    with cols[n+1]:
        db = pre['cons'][i][2] if (pre and i<len(pre['cons'])) else 0.0
        rhs = st.number_input('Vế phải', value=float(db), step=1.0,
                              key=f'b{i}', format='%g')
    constraints.append((row, OPMAP[op], rhs))

# ─── 3. Dấu biến ───────────────────────────────────────────────────────
st.subheader('3️⃣ Điều kiện dấu của biến')
signs=[]
cols=st.columns(n)
for j in range(n):
    ds = pre['signs'][j] if (pre and j<len(pre['signs'])) else 'x ≥ 0'
    with cols[j]:
        signs.append(SMAP[st.selectbox(f'x{j+1}', SIGNS,
                                       index=SIGNS.index(ds), key=f's{j}')])

# ─── Giải ──────────────────────────────────────────────────────────────
st.divider()
if st.button('🚀  GIẢI BÀI TOÁN', type='primary', use_container_width=True):
    try:
        res = solve(sense, [F(v) for v in obj],
                    [([F(x) for x in c], op, F(b)) for c,op,b in constraints],
                    signs, rule)
    except Exception as e:
        st.error(f'Lỗi: {e}'); st.stop()

    # ── Kết quả ────────────────────────────────────────────────────────
    st.subheader('📊 Kết quả')
    status = res['status']
    if status == 'optimal':
        st.success('✅ Bài toán CÓ nghiệm tối ưu.')
        c1, c2 = st.columns([1,2])
        with c1:
            st.metric('Giá trị tối ưu z*', fmt(res['opt_value']))
        with c2:
            st.write('**Nghiệm tối ưu:**')
            st.write(',   '.join(f'x{j+1} = {fmt(v)}'
                                  for j,v in enumerate(res['x'])))
        if res.get('multiple_optima'):
            st.info('ℹ️ Tồn tại biến phi cơ sở có hệ số 0 → có thể có **vô số nghiệm tối ưu**.')
        # ⑧ Suy biến
        if res.get('degenerate'):
            st.warning('⑧ **Suy biến:** có biến cơ sở = 0 tại nghiệm tối ưu. '
                       'Bài toán suy biến — nếu cần đảm bảo không xoay vòng, '
                       'hãy chọn quy tắc **Bland** ở thanh bên.')
    elif status == 'unbounded':
        st.warning('⚠️ Bài toán **KHÔNG BỊ CHẶN** (hàm mục tiêu → ±∞).')
    elif status == 'infeasible':
        st.error('❌ Bài toán **VÔ NGHIỆM** (miền ràng buộc rỗng).')

    # ④ Hình học
    if show_geo and int(n) == 2 and status in ('optimal','unbounded','infeasible'):
        st.subheader('④ Phương pháp hình học (2 biến)')
        try:
            fig = geo_draw(sense, obj, constraints, signs, res)
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f'Không vẽ được: {e}')

    # Cách đặt biến phụ
    with st.expander('ℹ️ Cách đặt biến phụ (đưa về dạng chuẩn)'):
        st.code(res.get('legend',''), language='text')

    # ⑥ Các từ vựng
    if show_dict and res.get('steps'):
        st.subheader('⑥ Các từ vựng từng bước')
        for k, stp in enumerate(res['steps'], 1):
            degen_tag = ' 🔸suy biến' if stp.get('degenerate_step') else ''
            with st.expander(
                f"Bước {k} · {stp['phase']}{degen_tag} · "
                f"vào: {stp['enter']} · ra: {stp['leave']}"):
                st.code(stp['dict_before'], language='text')
        if status == 'optimal':
            with st.expander('✅ Từ vựng cuối — NGHIỆM TỐI ƯU', expanded=True):
                st.code(res['final_dict'], language='text')
