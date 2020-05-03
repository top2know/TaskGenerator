from sympy import *
import numpy as np

from printer.printing import str_tree

MUL = 'mul'
ADD = 'add'
POW = 'pow'
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
    if type(expr) == symbol.Symbol \
            or type(expr) == numbers.One \
            or type(expr) == numbers.NegativeOne \
            or type(expr) == numbers.Zero \
            or type(expr) == numbers.Integer \
            or type(expr) == numbers.Float \
            or type(expr) == numbers.Half \
            or type(expr) == numbers.Rational:
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
    else:
        t = UNK
        val = [expr]
    return Tree(t, [create_tree(v) if t not in (SYM, UNK) else v for v in val])


def get_coeffs(expr, for_print=False):
    """
    Get parts of expression
    :param expr: expression
    :param for_print: JSON (print) support
    :return: dict {type: expr}
    """
    if not for_print and (type(expr) == symbol.Symbol
                          or type(expr) == numbers.NegativeOne
                          or type(expr) == numbers.Zero
                          or type(expr) == numbers.Integer
                          or type(expr) == numbers.Float
                          or type(expr) == numbers.Half
                          or type(expr) == numbers.Rational):
        return {'sym': expr}
    elif type(expr) == symbol.Symbol:
        return {'sym': str(expr)}
    elif type(expr) == numbers.One \
            or type(expr) == numbers.NegativeOne \
            or type(expr) == numbers.Zero \
            or type(expr) == numbers.Integer:
        return {'sym': int(expr)}
    elif type(expr) == numbers.Float \
            or type(expr) == numbers.Half \
            or type(expr) == numbers.Rational:
        return {'sym': float(expr)}
    elif type(expr) == power.Pow:
        return {'pow': list(expr.as_base_exp())}
    elif type(expr) == add.Add:
        t = 'add'
        arr = expr.as_coeff_add()
        res = [arr[0]] + list(arr[1]) if arr[0] != 0 else list(arr[1])
    elif type(expr) == mul.Mul:
        t = 'mul'
        arr = expr.as_coeff_mul()
        res = [arr[0]] + list(arr[1]) if arr[0] != 1 else list(arr[1])
    else:
        return {'unknown': [expr]}
    return {t: res}


def make_step(arr, for_print=False):
    """
    Recursive method for transforming SymPy to tree
    :param arr: parts of expression
    :param for_print: JSON (print) support
    :return: tree node
    """
    res = arr.copy()
    for k in res:
        if k not in ('unknown', 'sym'):
            for i in range(len(res[k])):
                res[k][i] = get_coeffs(res[k][i], for_print)
                if not 'sym' in res[k][i]:
                    res[k][i] = make_step(res[k][i], for_print)
    return res


def parse_sympy(expr, for_print=False):
    """
    Transforms SymPy expression to tree form
    :param expr:
    :param for_print:
    :return:
    """
    return make_step(get_coeffs(expr, for_print), for_print)


def parse_tree(d):
    """
    Transforms tree to SymPy expression
    :param d: tree mode
    :return: SymPy expression
    """
    if len(d) > 1:
        raise ValueError('')
    if 'mul' in d:
        return np.product([parse_tree(memb) for memb in d['mul']])
    if 'add' in d:
        return np.sum([parse_tree(memb) for memb in d['add']])
    if 'pow' in d:
        return parse_tree(d['pow'][0]) ** parse_tree(d['pow'][1])
    if 'sym' in d:
        return S(d['sym'])
    if 'unknown' in d:
        raise ValueError('unknown node found')
    raise ValueError('Unknown type {}'.format(d.keys()[0]))


def estimate_complexity(tree):
    """
    Estimates the complexity of the tree
    :param tree: tree node
    :return: the number representing the level of complexity
    """
    comp = 0

    if type(tree) is dict:
        for memb in tree.values():
            if type(memb) is list:
                for subtree in memb:
                    comp += estimate_complexity(subtree)
            else:
                comp += 1
    else:
        comp += 1
    return comp
