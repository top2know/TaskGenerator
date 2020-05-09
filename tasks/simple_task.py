import numpy as np
from tasks.task import AbstractTask, Task

data = [
    ['When was SE founded?', 2006],
    ['How many states are in USA?', 50],
    ['Some question', 'Some answer']
]


class SimpleTask(AbstractTask):
    """Example of class with predefined list of questions and answers"""
    def __init__(self, task='Simple'):
        """
        Constructor
        :param task: Name of task
        """
        super().__init__(task)

    def generate(self, params={}):
        rnd = np.random.randint(0, len(data))
        self.task = Task(data[rnd][0], '', data[rnd][1])
        return self.task


