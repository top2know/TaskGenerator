from generator import *
from generator.extenders import *
from sympy import *
from generator.generators import generator
from printer.printing import *

init_printing()

x = symbols('x')
for i in range(1, 43):
    print(i, make_fractions_pretty(generator(x+1, i)))


assert(extender_1(x+1).simplify() == x+1)
assert(extender_2(x+1).simplify() == x+1)
assert(extender_3(x+1).simplify() == x+1)
assert(extender_4(x+1).simplify() == x+1)
assert(extender_5(x+1).simplify() == x+1)
assert(extender_6(x+1).simplify() == x+1)

expr_to_pdf([generator(x + np.random.randint(-5, 6), 1 + np.random.randint(0, 61) % 6)
                                 for _ in range(5)], 'name', keep_file=True)

exp = 1.0*x

print(exp.as_coeff_mul()[1][0] == 1.0)
res = generator(x+1, 7)
print(res)
print(make_fractions_pretty(res))
print(remove_float_one(make_fractions_pretty(res)))
print(res.simplify())
print(make_fractions_pretty(res).simplify())
print(remove_float_one(make_fractions_pretty(res)).simplify())