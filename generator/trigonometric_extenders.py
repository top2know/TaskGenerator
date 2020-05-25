from generator.utils import *
from sympy.simplify.fu import TR8, TR9, TR11, TR2


class TrigonometryExtender:

    @staticmethod
    def trig_extender_1(expr, other_letters=False):
        """
        expr -> (sin*expr) / sin
        :param expr: expression
        :param other_letters: enable not 'x' letters
        :return: complicated expression
        """
        x = create_var(can_other_letters=other_letters, expr=expr)
        s = x * np.random.randint(1, 5)
        res = (2 * TR8(expr * sin(s))) / (2*sin(s))
        return res

    @staticmethod
    def trig_extender_2(expr, other_letters=False):
        """
        expr -> (cos*expr) / cos
        :param expr: expression
        :param other_letters: enable not 'x' letters
        :return: complicated expression
        """
        x = create_var(can_other_letters=other_letters, expr=expr)
        s = x * np.random.randint(1, 5)
        res = (2 * TR8(expr * cos(s))) / (2 * cos(s))
        return res

    @staticmethod
    def trig_extender_3(expr, other_letters=False):
        """
        sin(2x) -> 2sin(x)cos(x)
        :param expr: expression
        :param other_letters: enable not 'x' letters
        :return: complicated expression
        """
        res = TR11(expr)
        return res
