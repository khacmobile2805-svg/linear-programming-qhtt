# -*- coding: utf-8 -*-
"""solver.py — API cấp cao, trả kết quả đầy đủ cho giao diện."""
from fractions import Fraction
from ..models.problem import Problem
from .standardizer import standardize, describe_substitution, describe_standard
from .two_phase import solve_standard


def solve(sense, obj, constraints, var_signs, rule='dantzig') -> dict:
    """
    Giải QHTT tổng quát.
    rule: 'dantzig' (mặc định) | 'bland' (⑧ chống xoay vòng).
    """
    problem  = Problem.from_raw(sense, obj, constraints, var_signs)
    S        = standardize(problem)
    res      = solve_standard(S, rule)
    legend   = describe_substitution(S)

    if res['status'] in ('infeasible', 'unbounded', 'cycling'):
        return {'status': res['status'], 'steps': res['steps'], 'legend': legend,
                'standard_form': describe_standard(S)}

    D = res['dict']; ncol = len(S.var_names); m = len(S.A)
    vstd = [Fraction(0)]*ncol
    for i in range(m):
        if D.B[i] < ncol: vstd[D.B[i]] = D.b[i]
    x = [sum(mul*vstd[idx] for idx, mul in S.recover[j])
         for j in range(len(S.recover))]
    opt      = -D.z0 if S.was_max else D.z0
    multiple = any(D.d[j] == 0 for j in range(len(D.N)))
    # ⑧ phát hiện suy biến: biến cơ sở = 0 tại nghiệm tối ưu
    degenerate = any(D.b[i] == Fraction(0) for i in range(m))

    # ── KIỂM CHỨNG: thay nghiệm vào ràng buộc gốc + tính lại mục tiêu ──
    def _ok(op, lhs, rhs):
        return lhs <= rhs if op == '<=' else (lhs >= rhs if op == '>=' else lhs == rhs)
    checks = []
    for (co, op, rhs) in constraints:
        lhs = sum(Fraction(co[j]) * x[j] for j in range(len(x)))
        rhsf = Fraction(rhs)
        checks.append({'lhs': lhs, 'op': op, 'rhs': rhsf, 'ok': _ok(op, lhs, rhsf)})
    z_check = sum(Fraction(obj[j]) * x[j] for j in range(len(x)))
    all_ok = all(c['ok'] for c in checks)

    return {
        'status':          'optimal',
        'opt_value':       opt,
        'x':               x,
        'steps':           res['steps'],
        'final_dict':      D.render('z'),
        'legend':          legend,
        'multiple_optima': multiple,
        'degenerate':      degenerate,
        'standard_form':   describe_standard(S),
        'checks':          checks,
        'z_check':         z_check,
        'all_ok':          all_ok,
    }
