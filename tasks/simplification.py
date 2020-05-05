from sympy import simplify

from generator.SimplifyGenerator import SimplifyGenerator
from generator.extenders import create_var
from printer.printing import print_tex_on_html
from tasks.task import AbstractTask, Task
import numpy as np


def extract_val(arr, key, default=None):
    """
    Method for extracting params from dict
    :param arr: dict
    :param key: key to extract
    :param default: default value if key is missing
    :return: value of key or default
    """
    return arr[key] if key in arr and arr[key] else default


class SimplifyTask(AbstractTask):
    """Generator of Simplifying tasks"""

    def __init__(self, task='Simplify'):
        """
        Constructor
        :param task: Name of task
        :param var: number of simplification type
        """
        super().__init__(task)
        self.generator = SimplifyGenerator()

    def generate(self, params={}):
        """
        Generates the task
        :param params: dict of params
        :return:
        """
        xmin = extract_val(params, 'xmin', -5)
        xmax = extract_val(params, 'xmax', 5)
        roots = extract_val(params, 'roots', False)
        floats = extract_val(params, 'floats', False)
        other_letters = extract_val(params, 'other_letters', False)
        vars = extract_val(params, 'vars', 1)
        text = extract_val(params, 'text', '')
        min_comp = extract_val(params, 'min_comp', 10)
        max_comp = extract_val(params, 'max_comp', 30)
        x, y = create_var(can_other_letters=other_letters, can_root=roots, count=2)
        if vars == 1:
            answer = x + np.random.randint(xmin, xmax + 1)
        else:
            other_letters = True
            answer = x + y
        # todo remove complexity or define its usefulness
        expr, comp = self.generator.generate(answer,
                                             min_complexity=min_comp,
                                             max_complexity=max_comp,
                                             xmin=xmin,
                                             xmax=xmax,
                                             # todo add roots and floats to generator
                                             # roots=roots,
                                             # floats=floats,
                                             other_letters=other_letters
                                             )
        print(simplify(expr) == answer)
        self.task = Task(' '.join([text, str(comp)]), expr, answer)

    def to_html(self):
        """
        Turns task to HTML
        :return: HTML representation
        """
        return print_tex_on_html([self.task])
