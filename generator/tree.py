from sympy import *
import numpy as np

from printer.printing import str_tree

MUL = 'mul'
ADD = 'add'
POW = 'pow'
LOG = 'ln'
SIN = 'sin'
COS = 'cos'
TG = 'tg'
CTG = 'ctg'
SYM = 'sym'
UNK = 'unknown'


class Tree:
    """Tree representation of SymPy expression"""

    def __init__(self, operation, children=[]):
        self.operation = operation
        self.children = children

    def get_expr(self):
        if self.operation == MUL:
            return np.product([memb.get_expr() for memb in self.children])
        elif self.operation == ADD:
            return np.sum([memb.get_expr() for memb in self.children])
        elif self.operation == POW:
            return self.children[0].get_expr() ** self.children[1].get_expr()
        elif self.operation == LOG:
            return ln(self.children[0].get_expr())
        elif self.operation == SIN:
            return sin(self.children[0].get_expr())
        elif self.operation == COS:
            return cos(self.children[0].get_expr())
        elif self.operation == SYM:
            return S(self.children[0])
        elif self.operation == UNK:
            print(self.children)
            raise ValueError('unknown node found')
        raise ValueError('Unknown type {}'.format(self.operation))

    def get_complexity(self):

        complexity = 0

        if self.operation == SYM:
            complexity += 1
        else:
            for memb in self.children:
                complexity += memb.get_complexity()
        return complexity

    def get_json(self):
        if self.operation in (SYM, UNK):
            return {self.operation: str(self.children[0])}
        return {self.operation: [memb.get_json() for memb in self.children]}

    def print(self):
        return str_tree(self.get_json())


def create_tree(expr):
    """
    Get parts of expression
    :param expr: expression
    :return: dict {type: expr}
    """
    if type(expr) in (symbol.Symbol, numbers.One,
                      numbers.NegativeOne, numbers.Zero,
                      numbers.Integer, numbers.Float,
                      numbers.Half, numbers.Rational) \
            or type(expr) in (int, float):
        t = SYM
        val = [expr]
    elif type(expr) == power.Pow:
        t = POW
        val = list(expr.as_base_exp())
    elif type(expr) == add.Add:
        t = ADD
        arr = expr.as_coeff_add()
        val = [arr[0]] + list(arr[1]) if arr[0] != 0 else list(arr[1])
    elif type(expr) == mul.Mul:
        t = MUL
        arr = expr.as_coeff_mul()
        val = [arr[0]] + list(arr[1]) if arr[0] != 1 else list(arr[1])
    elif type(expr) == log:
        t = LOG
        val = list(expr.args)
    elif type(expr) == sin:
        t = SIN
        val = list(expr.args)
    elif type(expr) == cos:
        t = COS
        val = list(expr.args)
    else:
        t = UNK
        val = [expr]
    return Tree(t, [create_tree(v) if t not in (SYM, UNK) else v for v in val])
