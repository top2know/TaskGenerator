from sympy.core import *
from sympy.printing.latex import LatexPrinter
from sympy.core.function import _coeff_isneg
import numpy as np


class MyLatexPrinter(LatexPrinter):
    """Class for better-looking printing."""

    add_settings = {'order': 'normal'}

    def __init__(self, settings={}, add_settings={}):
        super().__init__(settings)
        for k in add_settings:
            self.add_settings[k] = add_settings[k]

    def _print_Add(self, expr, order=None):
        terms = self._as_ordered_terms(expr)
        if self.add_settings['order'] == 'reversed':
            terms = terms[::-1]
        elif self.add_settings['order'] == 'shuffle' or len(terms) == 2:
            np.random.shuffle(terms)

        tex = ""
        for i, term in enumerate(terms):
            if i == 0:
                pass
            elif _coeff_isneg(term):
                tex += " - "
                term = -term
            else:
                tex += " + "
            term_tex = self._print(term)
            if self._needs_add_brackets(term):
                term_tex = r"\left(%s\right)" % term_tex
            tex += term_tex

        return tex


def print_my_latex(expr):
    """
    LaTeX print ot pdflatex
    :param expr: expression
    :return: LaTeX expression
    """
    return '\[' + MyLatexPrinter().doprint(expr) + '\]'


def print_my_latex_html(expr, answer=None):
    """
    LaTeX print for HTML usage (KaTEX)
    :param expr: expression
    :param answer: simplified expression
    :return:
    """
    if answer:
        return MyLatexPrinter().doprint(Eq(expr, answer))
    else:
        return MyLatexPrinter().doprint(expr)


def make_fractions_pretty(expr, check=True):
    """
    a/c + b/c -> (a+b)/c
    :param expr: expression
    :param check: debug option
    :return: transformed expression
    """
    # TODO: works badly
    if type(expr) is not mul.Mul:
        if check:
            print('simple', type(expr), expr)
        return expr
    d = {}
    try:
        for memb in expr.as_coeff_mul()[1][-1].as_coeff_add()[1]:
            num, denom = memb.as_numer_denom()
            if denom in d:
                d[denom] += num
            else:
                d[denom] = num
        res = expr.as_coeff_mul()[0]*np.prod(expr.as_coeff_mul()[1][:-1]) * (expr.as_coeff_mul()[1][-1].as_coeff_add()[0]+np.sum([d[k] / k for k in d]))
        assert(res.simplify() == expr.simplify())
        return res
    except AssertionError:
        print('error while making pretty', res.simplify(), expr.simplify(), expr.as_coeff_mul()[1][-1], np.sum([d[k] / k for k in d]))
        return expr
    except:
        return expr


def remove_float_one(expr):
    """
    Solve the 1.0 problem of SymPy (1*x != 1.0*x)
    :param expr: expression
    :return: transformed expression
    """
    if type(expr) == mul.Mul:
        return expr.as_coeff_mul()[0] * np.prod(
            [remove_float_one(val) if val != S(1.0) else 1 for val in expr.as_coeff_mul()[1]])
    if type(expr) == add.Add:
        return expr.as_coeff_add()[0] + np.sum([remove_float_one(val) for val in expr.as_coeff_add()[1]])
    return expr


s = """"""


def str_tree(tree, level=0):
    """
    Tree printer
    :param tree: tree
    :param level: node level
    :return: string representation of tree
    """
    global s
    if level == 0:
        s = """"""
    for k in tree:
        s += ('----' * level + ' ' + k)
        if type(tree[k]) is list:
            s += '\r\n<br>'
            for memb in tree[k]:
                str_tree(memb, level=level+1)
        else:
            s += (': ' + str(tree[k]))
            s += """\r\n<br>"""
    if level == 0:
        return s


def make_pretty(expr, check=False):
    """
    Combines all methods of making expression pretty
    :param expr: expression
    :param check: debug purposes
    :return: prettier expression
    """

    p1 = make_fractions_pretty(expr, check)
    p2 = remove_float_one(p1)
    return p2


def print_tex_on_html(taskset, show_answers=False):
    """
    Prints expressions on HTML page
    :param taskset: list of Tasks
    :param show_answers: show answers for tasks
    :return: HTML code
    """
    texts = [task.get_condition() for task in taskset]
    tasks = [task.get_task() for task in taskset]
    answers = [task.get_answer() for task in taskset]
    s = "\n".join(["{}<div id = \"{}\">The expression was overcomplex</div><br>".format(texts[i] + '\n' if texts[i] else '', i) for i in range(len(tasks))])
    s += """<script>
    window.onload = function()
    {{
    """
    for i, res in enumerate(tasks):
        if show_answers:
            s += """katex.render(\"{}\", document.getElementById(\"{}\"));
""".format(print_my_latex_html(make_pretty(res, check=False), answers[i]).replace('\\', '\\\\'), i)
        else:
            s += """katex.render(\"{}\", document.getElementById(\"{}\"));
""".format(print_my_latex_html(make_pretty(res, check=False)).replace('\\', '\\\\'), i)
    s += """}}
    </script>"""
    return s

