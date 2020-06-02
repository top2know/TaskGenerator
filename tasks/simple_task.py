import numpy as np
from tasks.task import AbstractTask, Task

data = [
    ['Когда была основана ПИ?', 2006],
    ['Сколько штатов в США?', 50],
    ['Случайный вопрос', 'Случайный ответ'],
    ['Чему равно число пи?', 3.14159265],
    ['Ответ на главный вопрос жизни, вселенной и всего такого', 42]
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


