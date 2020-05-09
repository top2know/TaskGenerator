from tasks.equation import EquationTask
from tasks.simple_task import SimpleTask
from tasks.simplification import SimplifyTask
from tasks.task import AbstractTask


class TaskFactory:

    def get(self, name):
        if name == 'simplify':
            return SimplifyTask()
        if name == 'simple':
            return SimpleTask()
        if name == 'equation':
            return EquationTask()
        return AbstractTask()