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
    x = create_var(can_root=roots, can_other_letters=other_letters)
    a = x + S(c1)
    res = (expr * a).expand() / a
    return res



