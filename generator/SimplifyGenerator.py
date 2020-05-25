from generator.extenders import SimplifyExtender
from generator.tree import create_tree
import numpy as np
from sympy import simplify

from printer.printing import make_pretty


class SimplifyGenerator:

    def __init__(self, min_complexity=20, max_complexity=40):
        self.min_complexity = min_complexity
        self.max_complexity = max_complexity
        self.extender = SimplifyExtender()

    def extend(self, expr, xmin, xmax, other_letters, floats, roots):
        d = [f for f in self.extender.__dir__() if not f.endswith('__')]
        rnd = np.random.randint(0, len(d))
        return getattr(self.extender, d[rnd])(expr, n_min=xmin, n_max=xmax,
                                              other_letters=other_letters, floats=floats, roots=roots)

    @staticmethod
    def simplify(expr):
        tree = create_tree(expr)
        rnd = np.random.randint(0, len(tree.children))
        tree.children[rnd] = create_tree(simplify(tree.children[rnd].get_expr()))
        return tree.get_expr()

    def generate(self, expr, min_complexity=None, max_complexity=None, xmin=-20, xmax=20, other_letters=False, floats=False, roots=False):
        if not min_complexity:
            min_complexity = self.min_complexity
        if not max_complexity:
            max_complexity = self.max_complexity
        est = create_tree(expr).get_complexity()
        ans = expr
        counter = 0
        while est < min_complexity or est > max_complexity:
            if counter > 20:
                ans = expr
                counter = -1
            elif est < min_complexity:
                ans = self.extend(ans, xmin, xmax, other_letters, floats, roots)
            else:
                ans = self.simplify(ans)
            ans = make_pretty(ans)
            est = create_tree(ans).get_complexity()
            counter += 1
        return ans, est
