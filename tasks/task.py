from printer.printing import print_tex_on_html


class AbstractTask:
    """Abstract task with generation ability"""
    def __init__(self, name='Task'):
        """
        Constructor of abstract task
        :param name: name of task
        """
        self.name = name
        self.task = None

    def get(self, params=None):
        """
        Get concrete task, initialize if not exists
        :param params: dict of params
        :return: task
        """
        if not self.task:
            self.generate(params)
        return self.task

    def get_name(self):
        """Get name of task"""
        return self.name

    def generate(self, params):
        """
        Generate concrete task
        :param params: dict of params
        :return:
        """
        self.task = Task(params['condition'], params['task'], params['answer'])
        return self.task

    def to_html(self):
        """
        Turns task to HTML
        :return: HTML representation
        """
        return print_tex_on_html([self.task])


class Task:
    """Concrete task"""
    def __init__(self, condition, task, answer, params=None):
        """
        Constructor of task
        :param condition: text condition for the task
        :param task: SymPy expression
        :param answer: answer for the task
        :param params: dict of params
        """
        self.condition = condition
        self.task = task
        self.answer = answer
        self.params = params

    def get_answer(self):
        """
        Get answer
        :return: answer
        """
        return self.answer

    def get_task(self):
        """
        Get task
        :return: task (SymPy expression)
        """
        return self.task

    def get_condition(self):
        """
        Get condition
        :return: condition (text statement)
        """
        return self.condition

