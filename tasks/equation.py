import numpy as np
from sympy import Eq, solve

from generator.SimplifyGenerator import SimplifyGenerator
from generator.utils import create_var
from tasks.task import AbstractTask, Task


class EquationTask(AbstractTask):

    def __init__(self, task='Equation'):
        """
        Constructor
        :param task: Name of task
        :param var: number of simplification type
        """
        super().__init__(task)
        self.generator = SimplifyGenerator()

    def generate(self, params={}):
        x = create_var()
        expr = x + np.random.randint(-5, 6)

        task, comp = self.generator.generate(expr)

        answer = np.random.randint(3, 13)
        equation = Eq(task, answer)
        solutions = solve(equation, x)
        print(solutions)
        self.task = Task(str(comp), equation, ', '.join(list(map(str, solutions))))
        return self.task
