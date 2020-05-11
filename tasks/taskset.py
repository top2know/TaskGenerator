from printer.printing import print_tex_on_html, print_tex, print_tex_answers, print_tex_tasks


class TaskSet:
    """Contains list of abstract tasks while also generating the concrete ones"""
    def __init__(self, tasks, seed=42, init=False):
        """
        Initializes TaskSet
        :param tasks: array of (abstract) tasks
        :param seed: random seed
        :param init: if tasks are already initialized
        """
        self.tasks = tasks
        self.seed = seed
        if init:
            self.taskset = [[task.get() for task in tasks]]
        else:
            self.taskset = None

    def get(self, num=1, params=None):
        """
        Get taskset, generate if not exists
        :param num: number of variants
        :param params: dict of params
        :return: array of variants
        """
        if not self.taskset:
            self.generate(num, params)
        return self.taskset

    def generate(self, num=1, params=None):
        """
        Generate taskset
        :param num: number of variants
        :param params: dict of params
        :return:
        """
        self.taskset = [[task.generate(params) for task in self.tasks] for _ in range(num)]

    def to_html(self, num=0, show_answers=False):
        """
        Turns taskset to HTML
        :param num: number of variant
        :param show_answers: show answers for tasks
        :return: HTML representation
        """
        return print_tex_on_html(self.taskset[num], show_answers)

    def to_tex(self, multiple_files=True):
        files = []
        if multiple_files:
            for i in range(len(self.taskset)):
                files.append(print_tex(self.taskset[i], i))
        else:
            # todo
            files.append(print_tex_tasks(self.taskset))
        answers = print_tex_answers(self.taskset)
        return files, answers


