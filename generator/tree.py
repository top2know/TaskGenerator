from sympy import *
import numpy as np


def get_coeffs(expr, for_print=False):
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
    elif type(expr) == mul.Mul:
        t = 'mul'
        arr = expr.as_coeff_mul()
    else:
        return {'unknown': [expr]}
    return {t: [arr[0]] + list(arr[1])}


def make_step(arr, for_print=False):
    res = arr.copy()
    for k in res:
        if k not in ('unknown', 'sym'):
            for i in range(len(res[k])):
                res[k][i] = get_coeffs(res[k][i], for_print)
                if not 'sym' in res[k][i]:
                    res[k][i] = make_step(res[k][i], for_print)
    return res


def parse_sympy(expr, for_print=False):
    return make_step(get_coeffs(expr, for_print), for_print)


def parse_tree(d):
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
