from generator.utils import *
from sympy.simplify.fu import TR8, TR9


class TrigonometryExtender:

    @staticmethod
    def trig_extender_1(expr, other_letters=False):
        """
        expr -> (sin*expr) / sin
        :param expr: expression
        :param other_letters: enable not 'x' letters
        :return: complicated expression
        """
        x = create_var(can_other_letters=other_letters)
        s = x * np.random.randint(1, 5)
        res = TR8(expr * sin(s)) / sin(s)
        return res

    @staticmethod
    def trig_extender_2(expr, other_letters=False):
        """
        expr -> (cos*expr) / cos
        :param expr: expression
        :param other_letters: enable not 'x' letters
        :return: complicated expression
        """
        x = create_var(can_other_letters=other_letters)
        s = x * np.random.randint(1, 5)
        res = TR8(expr * cos(s)) / cos(s)
        return res
