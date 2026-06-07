# -*- coding: utf-8 -*-
"""
geometry.py — ④ Phương pháp hình học cho QHTT 2 biến.
Tịnh tiến hàm mục tiêu đến đỉnh tối ưu, vẽ miền chấp nhận được.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction


# ── Xây nửa mặt phẳng từ dữ liệu đầu vào ──────────────────────────────
def _build_halfplanes(constraints, var_signs):
    hps = []
    for j, s in enumerate(var_signs):
        a1, a2 = (1, 0) if j == 0 else (0, 1)
        if s == '>=0':
            hps.append({'a1': a1, 'a2': a2, 'op': '>=', 'b': 0, 'lbl': f'x{j+1} ≥ 0'})
        elif s == '<=0':
            hps.append({'a1': a1, 'a2': a2, 'op': '<=', 'b': 0, 'lbl': f'x{j+1} ≤ 0'})
    for i, (co, op, rhs) in enumerate(constraints):
        hps.append({'a1': float(co[0]), 'a2': float(co[1]),
                    'op': op, 'b': float(rhs), 'lbl': f'RB{i+1}'})
    return hps


def _intersect(h1, h2):
    a1, b1, c1 = h1['a1'], h1['a2'], h1['b']
    a2, b2, c2 = h2['a1'], h2['a2'], h2['b']
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-10:
        return None
    return ((c1*b2 - c2*b1)/det, (a1*c2 - a2*c1)/det)


def _ok(p, hps, eps=1e-7):
    x, y = p
    for h in hps:
        v = h['a1']*x + h['a2']*y
        if h['op'] == '<=' and v > h['b'] + eps: return False
        if h['op'] == '>=' and v < h['b'] - eps: return False
        if h['op'] == '='  and abs(v - h['b']) > eps*50: return False
    return True


def _vertices(hps):
    verts = []
    for i in range(len(hps)):
        for j in range(i+1, len(hps)):
            p = _intersect(hps[i], hps[j])
            if p and _ok(p, hps):
                dup = any(abs(p[0]-v[0]) < 1e-5 and abs(p[1]-v[1]) < 1e-5 for v in verts)
                if not dup:
                    verts.append(p)
    return verts


def _bbox(hps, verts):
    pts_x = [v[0] for v in verts]
    pts_y = [v[1] for v in verts]
    for h in hps:
        if abs(h['a1']) > 1e-9: pts_x.append(h['b'] / h['a1'])
        if abs(h['a2']) > 1e-9: pts_y.append(h['b'] / h['a2'])
    if pts_x:
        xlo, xhi = min(pts_x), max(pts_x)
        ylo, yhi = min(pts_y) if pts_y else xlo, max(pts_y) if pts_y else xhi
    else:
        xlo, xhi, ylo, yhi = -1, 10, -1, 10
    pad = max((xhi-xlo)*0.4, (yhi-ylo)*0.4, 2)
    return (max(xlo-pad, -20), min(xhi+pad, 30),
            max(ylo-pad, -20), min(yhi+pad, 30))


# ── Hàm chính ────────────────────────────────────────────────────────────
def draw(sense, obj, constraints, var_signs, solver_result):
    """
    Trả về matplotlib Figure cho bài toán 2 biến.
    solver_result: dict từ backend.core.solver.solve()
    """
    hps = _build_halfplanes(constraints, var_signs)
    verts = _vertices(hps)
    xlo, xhi, ylo, yhi = _bbox(hps, verts)

    # Lưới kiểm tra khả thi
    xs = np.linspace(xlo, xhi, 350)
    ys = np.linspace(ylo, yhi, 350)
    X, Y = np.meshgrid(xs, ys)
    mask = np.ones_like(X, dtype=bool)
    for h in hps:
        V = h['a1']*X + h['a2']*Y
        if h['op'] == '<=':  mask &= (V <= h['b'] + 1e-8)
        elif h['op'] == '>=': mask &= (V >= h['b'] - 1e-8)
        elif h['op'] == '=':
            tol = max(abs(h['b'])*0.015, 0.12)
            mask &= (np.abs(V - h['b']) <= tol)

    # Vẽ
    COLORS = ['#1f77b4','#d62728','#2ca02c','#9467bd','#8c564b','#e377c2','#17becf']
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(xlo, xhi); ax.set_ylim(ylo, yhi)

    if mask.any():
        ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5],
                    colors=['#a8d8a8'], alpha=0.45)

    xline = np.linspace(xlo, xhi, 300)
    for k, h in enumerate(hps):
        col = COLORS[k % len(COLORS)]
        if abs(h['a2']) > 1e-9:
            ax.plot(xline, (h['b'] - h['a1']*xline)/h['a2'],
                    '-', color=col, lw=1.4, label=h['lbl'])
        elif abs(h['a1']) > 1e-9:
            ax.axvline(h['b']/h['a1'], color=col, lw=1.4, label=h['lbl'])

    for v in verts:
        ax.plot(v[0], v[1], 'o', color='#333', ms=5, zorder=4)
        ax.annotate(f"({round(v[0],3)}, {round(v[1],3)})",
                    xy=v, xytext=(6, 4), textcoords='offset points', fontsize=7.5)

    status = solver_result['status']
    opt_label = ''
    if status == 'optimal':
        px = float(solver_result['x'][0])
        py = float(solver_result['x'][1])
        pz = float(solver_result['opt_value'])
        c1, c2 = float(obj[0]), float(obj[1])
        # Vẽ đường mức qua điểm tối ưu
        if abs(c2) > 1e-9:
            ax.plot(xline, (pz - c1*xline)/c2, '--', color='#c62828',
                    lw=1.5, alpha=0.8, label=f'z = {round(pz,4)}')
        # Đánh dấu điểm tối ưu
        ax.plot(px, py, '*', color='#c62828', ms=15, zorder=6,
                label=f'Tối ưu ({round(px,4)}, {round(py,4)})')
        opt_label = f"x₁ = {round(px,4)},  x₂ = {round(py,4)},  z* = {round(pz,4)}"
    elif status == 'unbounded':
        opt_label = '⚠ Bài toán KHÔNG BỊ CHẶN'
    elif status == 'infeasible':
        opt_label = '⚠ Bài toán VÔ NGHIỆM'

    ax.axhline(0, color='k', lw=0.6, alpha=0.4)
    ax.axvline(0, color='k', lw=0.6, alpha=0.4)
    c1t = f"{round(float(obj[0]),3)}"
    c2t = f"{round(float(obj[1]),3)}"
    ax.set_title(
        f"④ Phương pháp hình học — {sense} z = {c1t}x₁ + {c2t}x₂\n{opt_label}",
        fontsize=10)
    ax.set_xlabel('x₁', fontsize=11); ax.set_ylabel('x₂', fontsize=11)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.22)
    plt.tight_layout()
    return fig
