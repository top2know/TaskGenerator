from sympy.core import *
from pdflatex import PDFLaTeX
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


def print_my_latex_html(expr):
    """
    LaTeX print for HTML usage (KaTEX)
    :param expr:
    :return:
    """
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


def expr_to_pdf(res, name, keep_file=False):
    """
    Transforms list of expressions to PDF
    :param res: list of expressions
    :param name: File name
    :param keep_file: Save file locally
    :return: PDF file
    """
    content = r"""
\documentclass[a4paper]{}
\begin{}
{}
\end{}
""".format('{article}', '{document}',
           '\n\\newline\n'.join([print_my_latex(make_fractions_pretty(item, check=False)) for item in res]), '{document}')

    with open('temp.tex', 'w') as f:
        f.write(content)
    pdfl = PDFLaTeX.from_texfile('temp.tex')
    pdfl.set_pdf_filename(name)
    pdfl.set_output_directory('out')
    pdfl.set_jobname(name)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=keep_file)
    return pdf, log, completed_process


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
    :return: prettier expression
    """

    p1 = make_fractions_pretty(expr, check)
    p2 = remove_float_one(p1)
    return p2


def print_tex_on_html(tasks):
    """
    Prints expressions on HTML page
    :param tasks: list of expressions
    :return: HTML code
    """

    s = "\n".join(["<div id = \"{}\"></div><br>".format(i) for i in range(len(tasks))])
    s += """<script>
    window.onload = function()
    {{
    """
    for i, res in enumerate(tasks):
        s += """katex.render(\"{}\", document.getElementById(\"{}\"));
    """.format(print_my_latex_html(make_pretty(res, check=False)).replace('\\', '\\\\'), i)
    s += """}}
    </script>"""
    return s
