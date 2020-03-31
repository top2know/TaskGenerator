from generator.extenders import extender_1, extender_2


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
