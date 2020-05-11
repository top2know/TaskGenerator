from sympy import nsimplify
from sympy.core import *
from sympy.printing.latex import LatexPrinter
from sympy.core.function import _coeff_isneg
import numpy as np

from generator.tree import create_tree, SYM, UNK


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
        return expr
    d = {}
    try:
        for memb in expr.as_coeff_mul()[1][-1].as_coeff_add()[1]:
            num, denom = memb.as_numer_denom()
            if denom in d:
                d[denom] += num
            else:
                d[denom] = num
        res = expr.as_coeff_mul()[0] * np.prod(expr.as_coeff_mul()[1][:-1]) * (
                expr.as_coeff_mul()[1][-1].as_coeff_add()[0] + np.sum([d[k] / k for k in d]))
        assert (res.simplify() == expr.simplify())
        return res
    except AssertionError:
        print('error while making pretty', res.simplify(), expr.simplify(), expr.as_coeff_mul()[1][-1],
              np.sum([d[k] / k for k in d]))
        return expr
    except:
        return expr


def remove_float_one(expr):
    """
    Solve the 1.0 problem of SymPy (1*x != 1.0*x)
    :param expr: expression
    :return: transformed expression
    """
    return remove_floats(create_tree(expr)).get_expr()


def is_number(s):
    try:
        float(s)
        return True
    except TypeError:
        return False


def remove_floats(tree):
    if tree.operation in (SYM, UNK):
        if is_number(tree.children[0]) :
            if tree.children[0] == int(tree.children[0]):
                tree.children[0] = int(tree.children[0])
            elif len(str(tree.children[0]).rstrip('0')) > 5:
                print(nsimplify(tree.children[0]))
                tree.children[0] = nsimplify(tree.children[0])
    else:
        for i in range(len(tree.children)):
            remove_floats(tree.children[i])
    return tree


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
    s = "\n".join(
        ["{}<div id = \"{}\">The expression was overcomplex</div><br>".format(texts[i] + '\n' if texts[i] else '', i)
         for i in range(len(tasks))])
    s += """<script>
    window.onload = function()
    {{
    """
    for i, res in enumerate(tasks):
        if show_answers:
            s += """katex.render(\"{}\", document.getElementById(\"{}\"));
""".format(print_my_latex_html(res, answers[i]).replace('\\', '\\\\'), i)
        else:
            s += """katex.render(\"{}\", document.getElementById(\"{}\"));
""".format(print_my_latex_html(res).replace('\\', '\\\\'), i)
    s += """}}
    </script>"""
    return s


def print_tex(taskset, num):
    """
    Prints expressions on LaTeX page
    :param taskset: list of Tasks
    :return: LaTeX code
    """
    texts = [task.get_condition() for task in taskset]
    tasks = [task.get_task() for task in taskset]
    content = r"""\documentclass{0}
    \usepackage[utf8]{6}
    \usepackage[T2A,T1]{7}
    \usepackage[english,russian]{1}
    \begin{2}
    \begin{3} Вариант {4} \end{3} 
    \begin{5}
    {8}
    \end{5}
    \end{2}
    """.format('{article}', '{babel}', '{document}', '{center}', num, '{enumerate}', '{inputenc}', '{fontenc}',
               '\n'.join(['\\item ' + texts[i] + ' ' +
                          (print_my_latex(tasks[i]) if tasks[i] != '' else '') for i in
                          range(len(tasks))]))
    return content


def print_tex_answers(taskset):
    """
    Prints answers on LaTeX document
    :param taskset: list of Tasks
    :return: LaTeX code
    """
    answers = [[task.get_answer() for task in taskset[i]] for i in range(len(taskset))]
    content = r"""\documentclass{0}
        \usepackage[utf8]{1}
        \usepackage[T2A,T1]{2}
        \usepackage[english,russian]{3}
        \begin{4}
        {5}
        \end{4}
        """.format('{article}', '{inputenc}', '{fontenc}', '{babel}', '{document}',
                   '\n'.join([r"""\begin{0} Вариант {1} \end {0}
\begin{2}
{3}
\end{2}
\clearpage""".format('{center}', i, '{enumerate}',
              '\n'.join(['\\item ' + (answers[i][j] if (type(answers[i][j]) is str)
                                      else print_my_latex(answers[i][j]))
                         for j in range(len(answers[i]))]))
                              for i in range(len(taskset))]))

    return content


def print_tex_tasks(taskset):
    """
    Prints tasks on single LaTeX document
    :param taskset: list of Tasks
    :return: LaTeX code
    """
    texts = [[task.get_condition() for task in taskset[i]] for i in range(len(taskset))]
    tasks = [[task.get_task() for task in taskset[i]] for i in range(len(taskset))]
    content = r"""\documentclass{0}
        \usepackage[utf8]{1}
        \usepackage[T2A,T1]{2}
        \usepackage[english,russian]{3}
        \begin{4}
        {5}
        \end{4}
        """.format('{article}', '{inputenc}', '{fontenc}', '{babel}', '{document}',
                   '\n'.join([r"""\begin{0} Вариант {1} \end {0}
\begin{2}
{3}
\end{2}
\clearpage""".format('{center}', i, '{enumerate}',
              '\n'.join(['\\item ' + texts[i][j] + ' ' +
                         (print_my_latex(tasks[i][j]) if tasks[i][j] != '' else '')
                         for j in range(len(tasks[i]))]))
                              for i in range(len(taskset))]))

    return content
