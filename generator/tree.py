from sympy import *
import numpy as np


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
            or type(expr) == numbers.Half\
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




