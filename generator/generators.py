from generator.extenders import *


def generator(expr, mode=1):
    methods = [extender_1, extender_2, extender_3, extender_4, extender_5, extender_6]
    res = expr
    cur = mode
    try:
        while cur >= 0:
            res = methods[cur % len(methods)](res)
            cur //= len(methods)
            if cur == 0:
                break
            cur -= 1
        return res
    except AssertionError:
        print(expr, mode)
    except:
        print(expr, mode)
        raise Exception('Error while generating extenders', expr, mode)
