# -*- coding: utf-8 -*-
from enum import Enum
from fractions import Fraction


class ConstraintOp(Enum):
    LE = "<="
    GE = ">="
    EQ = "="


class Constraint:
    """Một ràng buộc:  coeffs · x  (op)  rhs."""
    def __init__(self, coeffs, op, rhs):
        self.coeffs = [Fraction(c) for c in coeffs]
        self.op = op if isinstance(op, ConstraintOp) else ConstraintOp(op)
        self.rhs = Fraction(rhs)

    def __repr__(self):
        lhs = " + ".join(f"{c}*x{i+1}" for i, c in enumerate(self.coeffs))
        return f"{lhs} {self.op.value} {self.rhs}"
