import numpy as np
from sympy import *


def one_const(n_min=-20, n_max=20, floats=False, roots=False):
    c1 = 0
    while c1 == 0:
        if not floats and not roots:
            c1 = np.random.randint(n_min, n_max + 1)
        elif floats and not roots:
            c1 = np.round((n_max - n_min) * np.random.random() + n_min, 1)
        elif not floats and roots:
            c1 = (-1) ** (np.random.randint(0, 2)) * sqrt(np.random.randint(0, n_max ** 2 + 1))
        else:
            if np.random.random() > 0.5:
                floats = False
            else:
                roots = False
    return c1


def two_const(n_min=-20, n_max=20, floats=False, roots=False):
    """
    Generate two distinct numbers
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: two numbers
    """
    c1, c2 = 0, 0
    while c1 == c2:
        if not floats and not roots:
            c1, c2 = np.random.randint(n_min, n_max + 1, 2)
        elif floats and not roots:
            c1, c2 = np.round((n_max - n_min) * np.random.random(size=2) + n_min, 1)
        elif not floats and roots:
            c1, c2 = (-1) ** (np.random.randint(0, 2)) * sqrt(np.random.randint(0, n_max ** 2 + 1)), \
                     (-1) ** (np.random.randint(0, 2)) * sqrt(np.random.randint(0, n_max ** 2 + 1))
        else:
            if np.random.random() > 0.5:
                floats = False
            else:
                roots = False
    if c1 == int(c1):
        c1 = int(c1)
    if c2 == int(c2):
        c2 = int(c2)
    return c1, c2


def create_var(can_root=False, can_other_letters=False, count=1, expr=None):
    """
    Create a variable
    :param count: number of variables
    :param can_root: x -> sqrt(x)
    :param can_other_letters: if variable can be not 'x'
    :return: variable
    """
    options = ['x', 'y']
    if expr and not can_other_letters:
        v = list(expr.expr_free_symbols)
    else:
        if can_other_letters:
            np.random.shuffle(options)
        letters = options[:count]
        v = [symbols(letter) for letter in letters]
    for i in range(len(v)):
        if can_root and np.random.rand() > 0.5:
            v[i] = sqrt(v[i])
    if count == 1:
        return v[0]
    else:
        return v[0], v[1]