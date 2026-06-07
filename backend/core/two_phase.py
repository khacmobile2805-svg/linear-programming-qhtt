# -*- coding: utf-8 -*-
"""two_phase.py — Điều phối đơn hình 2 pha, nhận thêm tham số rule."""
from fractions import Fraction
from .simplex import Dictionary, primal_simplex


def solve_standard(S, rule='dantzig') -> dict:
    m = len(S.A); ncol = len(S.var_names)
    steps = []

    D = Dictionary(m, ncol)
    for k in range(ncol): D.names[k] = S.var_names[k]
    for i in range(m):    D.names[ncol+i] = f'w{i+1}'
    D.N = list(range(ncol)); D.B = [ncol+i for i in range(m)]
    for i in range(m):
        D.b[i] = S.b[i]
        for j in range(ncol): D.a[i][j] = S.A[i][j]
    D.d = list(S.c); D.z0 = Fraction(0)

    need_p1 = any(bi < 0 for bi in S.b)
    if need_p1:
        X0 = 10**9; D.names[X0] = 'x0'
        D.N.append(X0)
        for i in range(m): D.a[i].append(Fraction(-1))
        saved_d = list(D.d)
        D.d = [Fraction(0)]*ncol + [Fraction(1)]; D.z0 = Fraction(0)
        l = min(range(m), key=lambda i: D.b[i]); e = len(D.N)-1
        steps.append({'phase': 'Pha 1', 'enter': 'x0', 'leave': D.names[D.B[l]],
                      'dict_before': D.render('δ'), 'degenerate_step': D.b[l]==0})
        D.pivot(l, e)
        primal_simplex(D, steps, 'Pha 1', 'δ', rule)
        if D.z0 > 0:
            return {'status': 'infeasible', 'steps': steps, 'dict': None}
        if X0 in D.B:
            li = D.B.index(X0)
            for j in range(len(D.N)):
                if D.N[j] != X0 and D.a[li][j] != 0:
                    D.pivot(li, j); break
        if X0 in D.N:
            jc = D.N.index(X0); D.N.pop(jc)
            for i in range(m): D.a[i].pop(jc)
        full = {k: Fraction(0) for k in range(ncol+m)}
        for j in range(ncol): full[j] = saved_d[j]
        D.z0 = sum(full.get(D.B[i], Fraction(0))*D.b[i] for i in range(m))
        D.d  = [full.get(D.N[j], Fraction(0)) -
                sum(full.get(D.B[i], Fraction(0))*D.a[i][j] for i in range(m))
                for j in range(len(D.N))]

    status = primal_simplex(D, steps, 'Pha 2' if need_p1 else 'Đơn hình', 'z', rule)
    if status == 'unbounded':
        return {'status': 'unbounded', 'steps': steps, 'dict': None}
    return {'status': 'optimal', 'steps': steps, 'dict': D}
