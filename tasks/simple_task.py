import numpy as np
from tasks.task import AbstractTask, Task

data = [
    ['When was SE founded?', 2006],
    ['How many states are in USA?', 50],
    ['Some question', 'Some answer']
]


class SimpleTask(AbstractTask):
    """Example of class with predefined list of questions and answers"""
    def __init__(self, task='Simple', params={}):
        """
        Constructor
        :param task: Name of task
        :param params: params for task
        """
        super().__init__(task)
        self.params = params

    def generate(self, params={}):
        rnd = np.random.randint(0, len(data))
        self.task = Task(data[rnd][0], '', data[rnd][1])
        return self.task


