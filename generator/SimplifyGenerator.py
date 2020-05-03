from generator.tree import estimate_complexity, parse_sympy, create_tree
from generator.generators import generator
import numpy as np
from sympy import simplify


class SimplifyGenerator:

    def __init__(self, min_complexity=20, max_complexity=40):
        self.min_complexity = min_complexity
        self.max_complexity = max_complexity

    @staticmethod
    def extend(expr, xmin, xmax, other_letters):
        return generator(expr, mode=np.random.randint(0, 6), nmin=xmin, nmax=xmax, other_letters=other_letters)

    @staticmethod
    def simplify(expr):
        tree = create_tree(expr)
        rnd = np.random.randint(0, len(tree.children))
        tree.children[rnd] = create_tree(simplify(tree.children[rnd].get_expr()))
        return tree.get_expr()

    def generate(self, expr, min_complexity=None, max_complexity=None, xmin=-20, xmax=20, other_letters=False):
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
                ans = self.extend(ans, xmin, xmax, other_letters)
            else:
                ans = self.simplify(ans)
            est = create_tree(ans).get_complexity()
            counter += 1
        return ans
