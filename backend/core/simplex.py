# -*- coding: utf-8 -*-
"""
simplex.py — ⑥⑧ Từ vựng (dictionary) + phép xoay + vòng lặp đơn hình.
Hỗ trợ hai quy tắc chọn biến vào:
  'dantzig' : hệ số ÂM NHẤT (mặc định, khớp ví dụ vở)
  'bland'   : chỉ số NHỎ NHẤT trong các hệ số âm (⑧ chống xoay vòng)
"""
from fractions import Fraction
from ..utils.formatting import fmt


class Dictionary:
    """
        x_{B[i]} = b[i] - Σ a[i][j] · x_{N[j]}
        z        = z0   + Σ d[j]   · x_{N[j]}        (đang MINIMIZE)
    """
    def __init__(self, m, n):
        self.B = [0]*m;  self.N = [0]*n
        self.a = [[Fraction(0)]*n for _ in range(m)]
        self.b = [Fraction(0)]*m
        self.d = [Fraction(0)]*n
        self.z0 = Fraction(0)
        self.names = {}

    def render(self, obj_label='z') -> str:
        def term(coef, name):
            if coef == 0: return None
            s = '+' if coef > 0 else '-'
            m = abs(coef); ms = '' if m == 1 else fmt(m)
            return f'{s} {ms}{name}' if ms else f'{s} {name}'
        lines = []
        parts = [f'{obj_label} = {fmt(self.z0)}']
        for j in range(len(self.N)):
            t = term(self.d[j], self.names[self.N[j]])
            if t: parts.append(t)
        lines.append(' '.join(parts)); lines.append('-'*44)
        for i in range(len(self.B)):
            parts = [f'{self.names[self.B[i]]} = {fmt(self.b[i])}']
            for j in range(len(self.N)):
                t = term(-self.a[i][j], self.names[self.N[j]])
                if t: parts.append(t)
            lines.append(' '.join(parts))
        return '\n'.join(lines)

    def pivot(self, l, e):
        oa = [r[:] for r in self.a]; ob = self.b[:]; od = self.d[:]
        piv = oa[l][e]
        self.B[l], self.N[e] = self.N[e], self.B[l]
        self.b[l] = ob[l] / piv
        for j in range(len(self.N)):
            self.a[l][j] = (Fraction(1)/piv) if j==e else oa[l][j]/piv
        for i in range(len(self.B)):
            if i == l: continue
            aie = oa[i][e]
            self.b[i] = ob[i] - aie*(ob[l]/piv)
            for j in range(len(self.N)):
                self.a[i][j] = (-aie/piv) if j==e else oa[i][j]-aie*(oa[l][j]/piv)
        de = od[e]
        self.z0 = self.z0 + de*(ob[l]/piv)
        for j in range(len(self.N)):
            self.d[j] = (-de/piv) if j==e else od[j]-de*(oa[l][j]/piv)


# ── Quy tắc chọn biến vào ────────────────────────────────────────────────
def choose_entering(D, rule='dantzig'):
    """
    'dantzig': hệ số âm nhất → khớp ví dụ vở.
    'bland'  : ⑧ chỉ số nhỏ nhất trong các cột âm → đảm bảo không xoay vòng.
    """
    neg = [j for j in range(len(D.N)) if D.d[j] < 0]
    if not neg:
        return -1
    if rule == 'bland':
        return min(neg, key=lambda j: D.N[j])
    # dantzig: âm nhất; bằng nhau → id nhỏ nhất
    best = min(D.d[j] for j in neg)
    cands = [j for j in neg if D.d[j] == best]
    return min(cands, key=lambda j: D.N[j])


def ratio_test(D, e):
    """Biến ra: tỉ số nhỏ nhất; bằng nhau → id nhỏ nhất (Bland leaving)."""
    l = -1; best = None; lid = None
    for i in range(len(D.B)):
        if D.a[i][e] > 0:
            r = D.b[i] / D.a[i][e]
            if best is None or r < best or (r == best and D.B[i] < lid):
                best = r; l = i; lid = D.B[i]
    return l, (best == Fraction(0)) if l != -1 else False


def primal_simplex(D, steps, phase_label, obj_label, rule='dantzig'):
    """Tối ưu hóa D. Trả về 'optimal'/'unbounded'."""
    while True:
        e = choose_entering(D, rule)
        if e == -1:
            return 'optimal'
        l, is_degen = ratio_test(D, e)
        if l == -1:
            return 'unbounded'
        steps.append({
            'phase': phase_label,
            'enter': D.names[D.N[e]],
            'leave': D.names[D.B[l]],
            'dict_before': D.render(obj_label),
            'degenerate_step': is_degen,   # ⑧ đánh dấu bước suy biến
        })
        D.pivot(l, e)
