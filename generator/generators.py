from generator.extenders import *


def generator(expr, mode=1):
    e1 = extender_1(expr)
    if mode == 1:
        return e1
    e2 = extender_2(expr)
    if mode == 2:
        return e2
    if mode == 3:
        return extender_1(e1)
    if mode == 4:
        return extender_1(e2)
    if mode == 5:
        return extender_2(e1)
    if mode == 6:
        return extender_2(e2)
    e3 = extender_3(expr)
    if mode == 7:
        return e3
    if mode == 8:
        return extender_1(e3)
    if mode == 9:
        return extender_2(e3)
    if mode == 10:
        return extender_3(e3)
    if mode == 11:
        return extender_3(e1)
    if mode == 12:
        return extender_3(e2)

