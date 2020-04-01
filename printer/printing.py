from sympy.core import *
from pdflatex import PDFLaTeX
from sympy.printing.latex import LatexPrinter
from sympy.core.function import _coeff_isneg
import numpy as np


class MyLatexPrinter(LatexPrinter):
    """Print better."""

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
    """ Most of the printers define their own wrappers for print().
    These wrappers usually take printer settings. Our printer does not have
    any settings.
    """
    return '\[' + MyLatexPrinter().doprint(expr) + '\]'


def make_fractions_pretty(expr, check=True):
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
        print('random exception')
        return expr


def remove_float_one(expr):
    if type(expr) == mul.Mul:
        return expr.as_coeff_mul()[0] * np.prod(
            [remove_float_one(val) if val != 1.0 else 1 for val in expr.as_coeff_mul()[1]])
    if type(expr) == add.Add:
        return expr.as_coeff_add()[0] + np.sum([remove_float_one(val) for val in expr.as_coeff_add()[1]])
    return expr


def expr_to_pdf(res, name, keep_file=False):
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
    pdfl.set_output_directory()
    pdfl.set_jobname(name)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=keep_file)
    return pdf, log, completed_process


s = """"""


def str_tree(tree, level=0):
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
