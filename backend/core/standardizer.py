# -*- coding: utf-8 -*-
"""Đưa bài toán tổng quát về DẠNG CHUẨN MIN: min c·v, A·v <= b, v >= 0."""
from fractions import Fraction
from ..models.variable import VariableSign
from ..models.constraint import ConstraintOp
from ..models.objective import ObjectiveSense
from ..models.standard_problem import StandardProblem
from ..utils.formatting import fmt


def standardize(problem) -> StandardProblem:
    n = problem.n
    S = StandardProblem()
    S.was_max = (problem.objective.sense == ObjectiveSense.MAX)

    # --- thay biến để mọi biến chuẩn đều >= 0 ---
    col_of = []
    for j, var in enumerate(problem.variables):
        if var.sign == VariableSign.NON_NEGATIVE:
            idx = len(S.var_names); S.var_names.append(f"x{j+1}")
            col_of.append([(idx, Fraction(1))])
        elif var.sign == VariableSign.NON_POSITIVE:          # x = -u, u >= 0
            idx = len(S.var_names); S.var_names.append(f"u{j+1}")
            col_of.append([(idx, Fraction(-1))])
        else:                                                # tự do = x+ - x-
            ip = len(S.var_names); S.var_names.append(f"x{j+1}p")
            im = len(S.var_names); S.var_names.append(f"x{j+1}m")
            col_of.append([(ip, Fraction(1)), (im, Fraction(-1))])
    S.recover = col_of
    ncol = len(S.var_names)

    # --- hàm mục tiêu: luôn quy về MIN ---
    c = [Fraction(0)] * ncol
    for j in range(n):
        coef = problem.objective.coeffs[j]
        for (idx, mul) in col_of[j]:
            c[idx] += coef * mul
    if S.was_max:                                            # max f = -min(-f)
        c = [-v for v in c]
    S.c = c

    # --- ràng buộc: mọi thứ về dạng <= ---
    def row_of(coeffs):
        r = [Fraction(0)] * ncol
        for j in range(n):
            cf = coeffs[j]
            for (idx, mul) in col_of[j]:
                r[idx] += cf * mul
        return r

    for con in problem.constraints:
        base = row_of(con.coeffs); rhs = con.rhs
        if con.op == ConstraintOp.LE:
            S.A.append(base);              S.b.append(rhs)
        elif con.op == ConstraintOp.GE:
            S.A.append([-v for v in base]); S.b.append(-rhs)
        else:                                                # = tách thành <= và >=
            S.A.append(base[:]);            S.b.append(rhs)
            S.A.append([-v for v in base]); S.b.append(-rhs)
    return S


def describe_substitution(S) -> str:
    """Giải thích cách đặt biến phụ (in trong báo cáo / giao diện)."""
    lines = []
    for j, cols in enumerate(S.recover):
        if len(cols) == 1 and cols[0][1] == 1:
            lines.append(f"x{j+1} = {S.var_names[cols[0][0]]}  (x{j+1} >= 0)")
        elif len(cols) == 1 and cols[0][1] == -1:
            lines.append(f"x{j+1} = -{S.var_names[cols[0][0]]}  (x{j+1} <= 0)")
        else:
            lines.append(f"x{j+1} = {S.var_names[cols[0][0]]} - {S.var_names[cols[1][0]]}  (x{j+1} tự do)")
    return "\n".join(lines)


def _lin(coeffs, names):
    parts = []
    for k, c in enumerate(coeffs):
        if c == 0: continue
        sgn = '+' if c > 0 else '-'
        mag = abs(c); ms = '' if mag == 1 else fmt(mag)
        term = f"{ms}{names[k]}" if ms else names[k]
        parts.append(term if not parts and sgn == '+' else f"{sgn} {term}")
    return " ".join(parts) if parts else "0"


def describe_standard(S) -> str:
    """In bài toán DẠNG CHUẨN min tương đương (để đưa vào báo cáo)."""
    names = S.var_names
    lines = [f"min  z = {_lin(S.c, names)}", "v.đk:"]
    for i in range(len(S.A)):
        lines.append(f"     {_lin(S.A[i], names)} <= {fmt(S.b[i])}")
    lines.append(f"     {', '.join(names)} >= 0")
    return "\n".join(lines)
