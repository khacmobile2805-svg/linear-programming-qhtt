# -*- coding: utf-8 -*-
"""Tiện ích định dạng."""
from fractions import Fraction


def fmt(x: Fraction) -> str:
    """Fraction -> chuỗi gọn: số nguyên bỏ mẫu, còn lại a/b."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
