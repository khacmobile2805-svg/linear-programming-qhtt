# -*- coding: utf-8 -*-
"""Bộ kiểm thử tự kiểm chứng — chạy: python test_cases.py"""
from fractions import Fraction as F
from backend.core.solver import solve


def run(sense, obj, cons, signs, rule='dantzig'):
    return solve(sense, [F(c) for c in obj],
                 [([F(x) for x in c],op,F(b)) for c,op,b in cons],
                 signs, rule)


CASES = [
    # status, opt, x                                 rule
    ('max cơ bản', 'max',[3,2],[([1,1],'<=',4),([1,3],'<=',6)],
     ['>=0','>=0'],'optimal',F(12),[F(4),F(0)],'dantzig'),
    ('min với >=','min',[2,3],[([1,1],'>=',10),([1,2],'>=',14)],
     ['>=0','>=0'],'optimal',F(24),[F(6),F(4)],'dantzig'),
    ('ràng buộc =','max',[4,3],[([2,3],'=',12),([1,1],'<=',5)],
     ['>=0','>=0'],'optimal',F(18),[F(3),F(2)],'dantzig'),
    ('biến tự do','max',[1,1],[([1,1],'<=',6),([1,-1],'<=',2)],
     ['free','>=0'],'optimal',F(6),[F(4),F(2)],'dantzig'),
    ('biến ≤0','max',[2,1],[([1,1],'<=',-1),([-1,2],'<=',4)],
     ['<=0','>=0'],'optimal',F(-2),[F(-1),F(0)],'dantzig'),
    ('không giới nội','max',[1,1],[([1,-1],'<=',1)],
     ['>=0','>=0'],'unbounded',None,None,'dantzig'),
    ('vô nghiệm','max',[1,1],[([1,1],'<=',2),([1,1],'>=',5)],
     ['>=0','>=0'],'infeasible',None,None,'dantzig'),
    ('2 pha (vở)','min',[5,-7],[([-4,1],'<=',-2),([1,1],'<=',5),([-1,-1],'<=',-1)],
     ['>=0','>=0'],'optimal',F(-91,5),[F(7,5),F(18,5)],'dantzig'),
    # ⑧ Bland cho cùng bài — phải cùng kết quả
    ('2 pha Bland','min',[5,-7],[([-4,1],'<=',-2),([1,1],'<=',5),([-1,-1],'<=',-1)],
     ['>=0','>=0'],'optimal',F(-91,5),[F(7,5),F(18,5)],'bland'),
    # ④ hình học max
    ('hình học max','max',[3,2],[([1,2],'<=',6),([2,1],'<=',8),([0,1],'<=',2)],
     ['>=0','>=0'],'optimal',F(38,3),[F(10,3),F(4,3)],'dantzig'),
]


def main():
    ok = 0
    for row in CASES:
        name,sense,obj,cons,signs,est,ez,ex,rule = row
        r = run(sense,obj,cons,signs,rule)
        assert r['status']==est, f'[{name}] status {r["status"]} != {est}'
        if est=='optimal':
            assert r['opt_value']==ez, f'[{name}] z* {r["opt_value"]} != {ez}'
            assert r['x']==ex,         f'[{name}] x {r["x"]} != {ex}'
        print(f'OK  {name}')
        ok += 1
    print(f'\n{ok}/{len(CASES)} test ĐẠT ✔')


if __name__ == '__main__':
    main()
