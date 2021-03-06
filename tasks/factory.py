from tasks.equation import EquationTask
from tasks.simple_task import SimpleTask
from tasks.simplification import SimplifyTask
from tasks.task import AbstractTask
from tasks.trigonometry import TrigonometricTask

params_easy = {
    'xmin': -5,
    'xmax': 5,
    'roots': False,
    'floats': False,
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 5,
    'max_comp': 14
}

params_medium = {
    'xmin': -10,
    'xmax': 10,
    'roots': False,
    'floats': False,
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 15,
    'max_comp': 25
}

params_hard = {
    'xmin': -20,
    'xmax': 20,
    'roots': False,
    'floats': False,
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 26,
    'max_comp': 42
}


trig_params_easy = {
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 8,
    'max_comp': 13
}

trig_params_medium = {
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 13.01,
    'max_comp': 21
}

trig_params_hard = {
    'vars': 1,
    'text': 'Упростите выражение: ',
    'min_comp': 21.01,
    'max_comp': 35
}


class TaskFactory:

    @staticmethod
    def get(name, comp='easy'):
        if name == 'simplify':
            if comp == 'easy':
                return SimplifyTask(params=params_easy)
            if comp == 'medium':
                return SimplifyTask(params=params_medium)
            if comp == 'hard':
                return SimplifyTask(params=params_hard)
            return SimplifyTask()
        if name == 'simple':
            return SimpleTask()
        if name == 'equation':
            if comp == 'easy':
                return EquationTask(params=params_easy)
            if comp == 'medium':
                return EquationTask(params=params_medium)
            if comp == 'hard':
                return EquationTask(params=params_hard)
            return EquationTask()
        if name == 'trig':
            if comp == 'easy':
                return TrigonometricTask(params=trig_params_easy)
            if comp == 'medium':
                return TrigonometricTask(params=trig_params_medium)
            if comp == 'hard':
                return TrigonometricTask(params=trig_params_hard)
            return TrigonometricTask()
        return AbstractTask()