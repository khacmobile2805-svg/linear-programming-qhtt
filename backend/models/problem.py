# -*- coding: utf-8 -*-
from .variable import Variable, VariableSign
from .constraint import Constraint, ConstraintOp
from .objective import Objective, ObjectiveSense


class Problem:
    """Bài toán QHTT TỔNG QUÁT."""
    def __init__(self, objective: Objective, constraints, variables):
        self.objective = objective
        self.constraints = list(constraints)
        self.variables = list(variables)

    @property
    def n(self):  # số biến
        return len(self.variables)

    @property
    def m(self):  # số ràng buộc
        return len(self.constraints)

    @classmethod
    def from_raw(cls, sense, obj, constraints, var_signs):
        """Dựng Problem từ dữ liệu thô (list) mà giao diện gửi xuống."""
        objective = Objective(obj, ObjectiveSense(sense))
        cons = [Constraint(c, op, b) for (c, op, b) in constraints]
        vrs = [Variable(f"x{j+1}", VariableSign(s)) for j, s in enumerate(var_signs)]
        return cls(objective, cons, vrs)
