import numpy as np
from sympy import Eq, solve

from generator.SimplifyGenerator import SimplifyGenerator
from generator.utils import create_var
from tasks.simplification import extract_val
from tasks.task import AbstractTask, Task


class EquationTask(AbstractTask):

    def __init__(self, task='Equation', params={}):
        """
        Constructor
        :param task: Name of task
        :param params: parameters for task
        """
        super().__init__(task)
        self.generator = SimplifyGenerator()
        self.params = params

    def generate(self, params=None):
        if not params:
            params = self.params
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
        task, comp = self.generator.generate(answer,
                                             min_complexity=min_comp,
                                             max_complexity=max_comp,
                                             xmin=xmin,
                                             xmax=xmax,
                                             # roots=roots,
                                             # floats=floats,
                                             other_letters=other_letters
                                             )

        answer = np.random.randint(3, 13)
        equation = Eq(task, answer)
        solutions = solve(equation, x)

        self.task = Task('Решите уравнение: ', equation, ', '.join(list(map(str, solutions))))
        #self.task = Task(' '.join([text, str(comp)]), equation, ', '.join(list(map(str, solutions))))
        return self.task
