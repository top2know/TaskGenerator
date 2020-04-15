from generator.extenders import *

methods = [extender_1, extender_2, extender_3, extender_4, extender_5, extender_6]


def generator(expr, mode=1, nmin=-20, nmax=20, floats=False, roots=False, other_letters=False):
    """
    Generates the complicated expression for the given
    :param expr: expression
    :param mode: algorithm of complication
    :param nmin: min value of const
    :param nmax: max value of const
    :param floats: enable floats
    :param roots: enable roots
    :param other_letters: enable not 'x' letter
    :return: complicated expression
    """
    res = expr
    cur = mode
    try:
        while cur >= 0:
            res = methods[cur % len(methods)](res, n_min=nmin, n_max=nmax, floats=floats, roots=roots, other_letters=other_letters)
            cur //= len(methods)
            if cur == 0:
                break
            cur -= 1
        return res
    except AssertionError:
        print(expr, mode)
    except:
        print(expr, mode)
        raise Exception('Error while generating extenders', expr, mode)


def generate_distinct(expr, floats=False, roots=False):
    """
    Complicates the expression by parts
    :param expr: expression
    :param floats: enable floats
    :param roots: enable roots
    :return: complicated expression
    """
    if type(expr) != add.Add:
        return generator(expr, np.random.randint(0, 42), floats, roots)

    modes = np.random.randint(0, len(methods), len(expr.as_coeff_add()[1]))
    return np.sum([methods[modes[i]](v, floats=floats, roots=roots) for i, v in enumerate(expr.as_coeff_add()[1])])+expr.as_coeff_add()[0]
