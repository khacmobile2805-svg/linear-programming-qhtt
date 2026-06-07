# -*- coding: utf-8 -*-
from enum import Enum
from fractions import Fraction


class ObjectiveSense(Enum):
    MIN = "min"
    MAX = "max"


class Objective:
    """Hàm mục tiêu:  (min/max)  coeffs · x."""
    def __init__(self, coeffs, sense=ObjectiveSense.MIN):
        self.coeffs = [Fraction(c) for c in coeffs]
        self.sense = sense if isinstance(sense, ObjectiveSense) else ObjectiveSense(sense)
