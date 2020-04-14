import numpy as np
from sympy import *


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


def create_var(can_root=False, can_other_letters=False):
    """
    Create a variable
    :param can_root: x -> sqrt(x)
    :param can_other_letters: if variable can be not 'x'
    :return: variable
    """
    if can_other_letters:
        letter = np.random.choice(['x', 'y', 'a'])
    else:
        letter = 'x'
    v = symbols(letter)
    if can_root and np.random.rand() > 0.5:
        v = sqrt(v)
    return v


def extender_1(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """
    expr -> (1+(b-a)/a)*((expr*a)/b)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1, c2 = two_const(n_min, n_max, floats, roots)
    # TODO: in place of a and b there can be any function
    x = create_var(can_root=roots)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr * a).expand() / b
    second = 1 + (b - a) / a
    res = first * second
    return res


def extender_2(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """expr -> ((expr*b)/a) / (k/b + k/a + (x^2+k^2)/(a*b))
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
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
    x = create_var(can_root=roots)
    a = x - S(c1)
    b = x + S(c1)
    first = (expr * b).expand() / a
    k = S(c1)
    second = 1 / (k / b - k / -a + (x ** 2 + k ** 2) / (a * b).expand())
    res = first * second
    return res


def extender_3(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """expr -> ((expr*a/2)/a)+(expr*a*b)/(2*a*b)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1, c2 = two_const(n_min, n_max, floats, roots)
    # TODO: in place of a and b there can be any function
    x = create_var(can_root=roots)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr / 2 * a).expand() / a
    second = (expr * a * b).expand() / (2 * a * b).expand()
    res = first + second
    # assert (res.simplify() == expr.simplify())
    return res


def extender_4(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """expr -> (cb+b(b-ac)/a)*((expr*a)/b^2)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1, c2 = two_const(n_min, n_max, floats, roots)
    # TODO: in place of a and b there can be any function
    x = create_var(can_root=roots)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr * a).expand() / (b ** 2)
    c = 0
    while c == 0:
        c = np.random.randint(n_min, n_max)
    second = c * b + (b * (b - c * a)).expand() / a
    res = first * second
    # assert (res.simplify() == expr.simplify())
    return res


def extender_5(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """expr -> (c+(b-ca)/a)*((expr*a)/b)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1, c2 = two_const(n_min, n_max, floats, roots)
    # TODO: in place of a and b there can be any function
    x = create_var(can_root=roots)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr * a).expand() / b
    c = 0
    while c == 0 or c == 1:
        c = np.random.randint(n_min, n_max)
    second = c + (b - c * a).expand() / a
    res = first * second
    # assert (res.simplify() == expr.simplify())
    return res


def extender_6(expr, n_min=-20, n_max=20, floats=False, roots=False):
    """expr -> (c/b+(1-ca/b)/a)*(expr*a)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1, c2 = two_const(n_min, n_max, floats, roots)
    # TODO: in place of a and b there can be any function
    x = create_var(can_root=roots)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr * a).expand()
    c = 0
    while c == 0 or c == 1:
        c = np.random.randint(n_min, n_max)
    second = c / b + (1 - (c * a).expand() / b) / a
    res = first * second
    # assert (res.simplify() == expr.simplify())
    return res
