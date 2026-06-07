# -*- coding: utf-8 -*-
class StandardProblem:
    """Bài toán đã đưa về DẠNG CHUẨN MIN:  min c·v ,  A·v <= b ,  v >= 0."""
    def __init__(self):
        self.c = []           # hệ số mục tiêu (dạng MIN)
        self.A = []           # ma trận ràng buộc (đều dạng <=)
        self.b = []           # vế phải
        self.var_names = []   # tên biến cấu trúc
        self.recover = []     # biến gốc j = sum(mul * v[idx])
        self.was_max = False  # bài gốc là max?
