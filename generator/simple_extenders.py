from generator.utils import *


def simple_extender_1(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> (expr*(x+a))/(x+a)
    :param expr: expression
    :param n_min: min value of const
    :param n_max: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :param other_letters: enable not 'x' letters
    :return: complicated expression
    """
    if n_min >= n_max:
        raise ValueError('n_min ({}) should be less than n_max ({})'.format(n_min, n_max))
    c1 = one_const(n_min, n_max, floats, roots)
    x = create_var(can_root=roots, can_other_letters=other_letters)
    a = x + S(c1)
    res = (expr * a).expand() / a
    return res



