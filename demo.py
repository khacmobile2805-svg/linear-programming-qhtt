# -*- coding: utf-8 -*-
"""demo.py — chạy dòng lệnh, in từ vựng của 3 phương pháp."""
from fractions import Fraction as F
from backend.core.solver import solve
from backend.utils.formatting import fmt


def show(title, sense, obj, cons, signs, rule='dantzig'):
    print('='*60); print(title); print('='*60)
    r = solve(sense,[F(c) for c in obj],
              [([F(x) for x in c],op,F(b)) for c,op,b in cons], signs, rule)
    for k, s in enumerate(r['steps'], 1):
        tag = ' [SUYBIẾN]' if s.get('degenerate_step') else ''
        print(f"[{s['phase']}] Bước {k}{tag}: vào {s['enter']}, ra {s['leave']}")
        print(s['dict_before']); print()
    if r['status'] == 'optimal':
        print('TỪ VỰNG TỐI ƯU:'); print(r['final_dict'])
        print(f"z* = {fmt(r['opt_value'])} | "
              + ', '.join(f'x{i+1}={fmt(v)}' for i,v in enumerate(r['x'])))
        if r.get('degenerate'): print('[⑧ Suy biến tại nghiệm tối ưu]')
    else:
        print('Kết luận:', r['status'])
    print()


if __name__ == '__main__':
    # ④⑥ Hình học + đơn hình
    show('④⑥ max 3x1+2x2 (1 pha, hình học)', 'max', [3,2],
         [([1,2],'<=',6),([2,1],'<=',8),([0,1],'<=',2)], ['>=0','>=0'])

    # ⑨ 2 pha (từ vở)
    show('⑨ min 5x1-7x2 (2 pha)', 'min', [5,-7],
         [([-4,1],'<=',-2),([1,1],'<=',5),([-1,-1],'<=',-1)], ['>=0','>=0'])

    # ⑧ Bland trên bài suy biến
    show('⑧ Bland — bài suy biến: max 2x1+3x2', 'max', [2,3],
         [([2,1],'<=',14),([1,2],'<=',14),([1,1],'<=',8),([1,0],'<=',6)],
         ['>=0','>=0'], rule='bland')
