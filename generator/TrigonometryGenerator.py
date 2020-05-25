from generator.trigonometric_extenders import TrigonometryExtender
from generator.tree import create_tree, SYM, UNK, SIN, COS
import numpy as np
from sympy import simplify, trigsimp

from printer.printing import make_pretty


class TrigonometryGenerator:

    def __init__(self, min_complexity=20, max_complexity=40):
        self.min_complexity = min_complexity
        self.max_complexity = max_complexity
        self.extender = TrigonometryExtender()

    def extend(self, tree, other_letters):
        d = [f for f in self.extender.__dir__() if not f.endswith('__')]
        r = np.random.randint(0, len(d))
        if tree.operation in (SYM, UNK):
            return tree
        if tree.operation in (SIN, COS):
            return create_tree(getattr(self.extender, d[r])(tree.get_expr(),
                                                                     other_letters=other_letters))
        cur = tree
        rnd = np.random.randint(0, len(cur.children))
        while cur.children[rnd].operation not in (SIN, COS):
            if cur.children[rnd].operation in (SYM, UNK):
                cur = tree
                break
            else:
                cur = cur.children[rnd]
            rnd = np.random.randint(0, len(cur.children))
        cur.children[rnd] = create_tree(getattr(self.extender, d[r])(cur.children[rnd].get_expr(),
                                                                     other_letters=other_letters))
        return tree

    @staticmethod
    def simplify(tree):
        est = tree.get_complexity()
        counter = 0
        while tree.get_complexity() == est and counter < 5:
            rnd = np.random.randint(0, len(tree.children))
            tree.children[rnd] = create_tree(trigsimp(tree.children[rnd].get_expr()))
            counter += 1
        if est == tree.get_complexity():
            return False
        return tree

    def generate(self, expr, min_complexity=None, max_complexity=None, other_letters=False):
        if not min_complexity:
            min_complexity = self.min_complexity
        if not max_complexity:
            max_complexity = self.max_complexity
        ans = create_tree(expr)
        est = ans.get_complexity()
        counter = 0
        while est < min_complexity or est > max_complexity:
            exp = ans.get_expr()
            if counter > 20:
                break
                ans = create_tree(expr)
                counter = -1
            elif est < min_complexity:
                ans = self.extend(ans, other_letters)
            else:
                ans = self.simplify(ans)
            if not ans:
                ans = create_tree(expr)
                counter = -1
            ans = create_tree(ans.get_expr())
            est = ans.get_complexity()
            counter += 1
        return ans.get_expr(), est
