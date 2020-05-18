from sympy import simplify, sin, cos

from generator.TrigonometryGenerator import TrigonometryGenerator
from generator.extenders import create_var
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
    return arr[key] if arr and key in arr and arr[key] else default


class TrigonometricTask(AbstractTask):
    """Generator of Trigonometry tasks"""

    def __init__(self, task='Trigonometry', params={}):
        """
        Constructor
        :param task: Name of task
        :param params: parameters for task
        """
        super().__init__(task)
        self.generator = TrigonometryGenerator()
        self.params = params

    def generate(self, params=None):
        """
        Generates the task
        :param params: dict of params
        :return:
        """
        if not params:
            params = self.params
        other_letters = extract_val(params, 'other_letters', False)
        text = extract_val(params, 'text', '')
        min_comp = extract_val(params, 'min_comp', 10)
        max_comp = extract_val(params, 'max_comp', 30)
        vars = extract_val(params, 'vals', 1)
        x, y = create_var(can_other_letters=other_letters, count=2)
        if vars == 1:
            if np.random.rand() > 0.5:
                answer = sin(x)
            else:
                answer = cos(x)
        else:
            other_letters = True
            answer = sin(x) + cos(y)
        # todo remove complexity or define its usefulness
        expr, comp = self.generator.generate(answer,
                                             min_complexity=min_comp,
                                             max_complexity=max_comp,
                                             other_letters=other_letters
                                             )
        self.task = Task(' '.join([text, str(comp)]), expr, answer)
        return self.task

