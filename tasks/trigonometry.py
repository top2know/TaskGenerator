from sympy import simplify, sin, cos, tan

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
        x *= np.random.randint(1, 2)
        y *= np.random.randint(1, 2)
        if vars == 1:
            rnd = np.random.rand()
            if rnd > 0.8:
                answer = sin(x)
            elif rnd > 0.6:
                answer = cos(x)
            elif rnd > 0.4:
                answer = sin(y)
            elif rnd > 0.2:
                answer = cos(y)
            elif rnd > 0.1:
                answer = sin(x)
            else:
                answer = cos(y)
        else:
            other_letters = True
            answer = sin(x) + cos(y)
        # todo remove complexity or define its usefulness
        expr, comp = self.generator.generate(answer,
                                             min_complexity=min_comp,
                                             max_complexity=max_comp,
                                             other_letters=other_letters
                                             )
        #self.task = Task('Упростите выражение: ', expr, answer)
        self.task = Task(' '.join([text, str(comp)]), expr, answer)
        print(str(comp), expr, answer)
        return self.task

