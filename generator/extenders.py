from generator.simple_extenders import simple_extender_1
from generator.utils import *


def extender_1(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """
    expr -> (1+(b-a)/a)*((expr*a)/b)
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
    c1, c2 = two_const(n_min, n_max, floats, roots)

    x = create_var(can_root=roots, can_other_letters=other_letters)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr * a).expand() / b
    second = 1 + (b - a) / a
    res = first * second
    return res


def extender_2(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> ((expr*b)/a) / (k/b + k/a + (x^2+k^2)/(a*b))
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
    a = x - S(c1)
    b = x + S(c1)
    first = (expr * b).expand() / a
    k = S(c1)
    second = 1 / (k / b - k / -a + (x ** 2 + k ** 2) / (a * b).expand())
    res = first * second
    return res


def extender_3(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> ((expr*a/2)/a)+(expr*a*b)/(2*a*b)
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
    c1, c2 = two_const(n_min, n_max, floats, roots)

    x = create_var(can_root=roots, can_other_letters=other_letters)
    a = x + S(c1)
    b = x + S(c2)
    first = (expr / 2 * a).expand() / a
    second = (expr * a * b).expand() / (2 * a * b).expand()
    res = first + second
    # assert (res.simplify() == expr.simplify())
    return res


def extender_4(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> (cb+b(b-ac)/a)*((expr*a)/b^2)
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
    c1, c2 = two_const(n_min, n_max, floats, roots)

    x = create_var(can_root=roots, can_other_letters=other_letters)
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


def extender_5(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> (c+(b-ca)/a)*((expr*a)/b)
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
    c1, c2 = two_const(n_min, n_max, floats, roots)

    x = create_var(can_root=roots, can_other_letters=other_letters)
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


def extender_6(expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
    """expr -> (c/b+(1-ca/b)/a)*(expr*a)
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
    c1, c2 = two_const(n_min, n_max, floats, roots)

    x = create_var(can_root=roots, can_other_letters=other_letters)
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


class SimplifyExtender:

    def extender_1(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_1(expr, n_min, n_max, floats, roots, other_letters)

    def extender_2(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_2(expr, n_min, n_max, floats, roots, other_letters)

    def extender_3(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_3(expr, n_min, n_max, floats, roots, other_letters)

    def extender_4(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_4(expr, n_min, n_max, floats, roots, other_letters)

    def extender_5(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_5(expr, n_min, n_max, floats, roots, other_letters)

    def extender_6(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return extender_6(expr, n_min, n_max, floats, roots, other_letters)

    def simple_extender_1(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        return simple_extender_1(expr, n_min, n_max, floats, roots, other_letters)

    def extender_1_distinct(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        d = [f for f in self.__dir__() if not f.endswith('__') and not f.endswith('distinct')]
        if type(expr) != add.Add:
            return getattr(self, d[np.random.randint(0, len(d))])(expr, n_min, n_max, floats, roots, other_letters)
        modes = np.random.randint(0, len(d), len(expr.as_coeff_add()[1]))
        return np.sum(
            [getattr(self, d[modes[i]])(v, n_min=n_min, n_max=n_max, floats=floats, roots=roots,
                                        other_letters=other_letters)
             for i, v in enumerate(expr.as_coeff_add()[1])]) + \
               expr.as_coeff_add()[0]

    def extender_2_distinct(self, expr, n_min=-20, n_max=20, floats=False, roots=False, other_letters=False):
        d = [f for f in self.__dir__() if not f.endswith('__') and not f.endswith('distinct')]
        if type(expr) != add.Add:
            return getattr(self, d[np.random.randint(0, len(d))])(expr, n_min, n_max, floats, roots, other_letters)
        modes = np.random.randint(0, len(d), 2)
        count, additions = expr.as_coeff_add()[0], expr.as_coeff_add()[1]
        rnd = np.random.randint(n_min, n_max)
        while rnd == count or rnd == 0:
            rnd = np.random.randint(n_min, n_max)
        a = rnd
        b = count - rnd
        for memb in additions:
            if type(memb) == mul.Mul:
                coeff = memb.as_coeff_mul()[0]
                rnd = np.random.randint(n_min, n_max)
                while rnd == coeff or rnd == 0:
                    rnd = np.random.randint(n_min, n_max)
                a += rnd / coeff * memb
                b += (coeff - rnd) / coeff * memb
            elif type(memb) == Symbol:
                rnd = np.random.randint(n_min, n_max)
                a += rnd * memb
                b -= (rnd - 1) * memb
            elif np.random.rand() > 0.5:
                a += memb
            else:
                b += memb
        return getattr(self, d[modes[0]])(a, n_min=n_min, n_max=n_max,
                                          floats=floats, roots=roots,
                                          other_letters=other_letters) + getattr(self, d[modes[1]])(b, n_min=n_min,
                                                                                                    n_max=n_max,
                                                                                                    floats=floats,
                                                                                                    roots=roots,
                                                                                                    other_letters=other_letters)
