# -*- coding: utf-8 -*-
from enum import Enum


class VariableSign(Enum):
    """Dấu của biến."""
    NON_NEGATIVE = ">=0"   # x >= 0
    NON_POSITIVE = "<=0"   # x <= 0
    FREE = "free"          # x tự do


class Variable:
    """Một biến quyết định: tên + điều kiện dấu."""
    def __init__(self, name: str, sign: VariableSign = VariableSign.NON_NEGATIVE):
        self.name = name
        self.sign = sign if isinstance(sign, VariableSign) else VariableSign(sign)

    def __repr__(self):
        if self.sign == VariableSign.FREE:
            return f"{self.name} tự do"
        return f"{self.name} {self.sign.value}"
