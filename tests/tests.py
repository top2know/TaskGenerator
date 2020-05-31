import unittest

from generator.SimplifyGenerator import SimplifyGenerator
from generator.TrigonometryGenerator import TrigonometryGenerator
from generator.generators import *
from generator.trigonometric_extenders import TrigonometryExtender
from printer.printing import *
from generator.tree import create_tree, complexities, SIN, MUL
from tasks.factory import TaskFactory
from tasks.taskset import TaskSet


class UnitTest(unittest.TestCase):

    def setUp(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.methods = [extender_1,
                        extender_2,
                        extender_3,
                        extender_4,
                        extender_5,
                        extender_6]

    def test_check_extenders_simple(self):
        x = self.x
        ans = x + 1
        for method in self.methods:
            self.assertNotEqual(ans, method(ans))
            self.assertEqual(ans, method(ans).simplify())

    @unittest.expectedFailure
    def test_check_extenders_roots(self):
        x = self.x
        ans = x + 1
        for method in self.methods:
            self.assertNotEqual(ans, method(ans, roots=True))
            self.assertEqual(ans, method(ans, roots=True).simplify())

    def test_check_generators_distinct(self):
        x = self.x
        y = self.y
        ans = x + y
        res = generate_distinct(ans)
        self.assertNotEqual(ans, res)
        self.assertEqual(ans, remove_float_one(res.simplify()))

    @unittest.expectedFailure
    def test_check_extenders_floats(self):
        x = self.x
        ans = x + 2
        for method in self.methods:
            res = method(ans, floats=True)
            self.assertNotEqual(ans, res)
            self.assertEqual(ans, remove_float_one(res.simplify()))

    def test_check_generators_simple(self):
        x = self.x
        for i in range(len(self.methods) * (len(self.methods) + 1)):
            ans = x + np.random.randint(-5, 6)
            gen = generator(ans, i)
            self.assertNotEqual(ans, gen)
            self.assertEqual(ans, gen.simplify())

    @unittest.expectedFailure
    def test_check_generators_roots(self):
        x = self.x
        for i in range(len(self.methods) * (len(self.methods) + 1)):
            ans = x + np.random.randint(-5, 6)
            gen = generator(ans, i, roots=True)
            self.assertNotEqual(ans, gen)
            self.assertEqual(ans, gen.simplify())

    def test_routes(self):
        from app import app
        with app.test_client() as client:
            self.assertEqual('200 OK', client.get('/news').status)
            self.assertEqual('200 OK', client.get('/tree').status)
            self.assertEqual('200 OK', client.get('/menu').status)
            self.assertEqual('200 OK', client.get('/generate_taskset').status)
            self.assertEqual('200 OK', client.get('/generate_demo_taskset').status)

    def test_tree_complexity(self):
        x = self.x
        self.assertEqual(1, create_tree(1).get_complexity())
        self.assertEqual(2, create_tree(x + 1).get_complexity())
        self.assertEqual(4, create_tree(x**2 + x + 1).get_complexity())

    def test_tree(self):
        x = self.x
        expr = (x**3 + 2*x**2)/(x+3)
        tree = create_tree(expr)
        self.assertEqual(MUL, tree.operation)
        self.assertEqual(expr, tree.get_expr())

    def test_generator(self):
        generator = SimplifyGenerator(35, 50)
        print(generator.generate(self.x + 1))
        ext = SimplifyExtender()
        g = ext.extender_2_distinct(self.x + 1)
        print(g)
        self.assertEqual(self.x + 1, simplify(g))

    @unittest.expectedFailure
    def test_trig_generator(self):
        generator = TrigonometryGenerator(50, 70)
        for _ in range(10):
            ans = sin(self.x)
            expr, comp = generator.generate(sin(self.x))
            self.assertEqual(ans, trigsimp(expr))

    def test_trig_extenders(self):
        extender = TrigonometryExtender()
        methods = [f for f in extender.__dir__() if not f.endswith('__')]
        for method in methods:
            ans = sin(1)
            expr = getattr(extender, method)(ans)
            self.assertEqual(ans, trigsimp(expr))
            ans = cos(1)
            expr = getattr(extender, method)(ans)
            self.assertEqual(ans, trigsimp(expr))

    def test_trig_complexity(self):
        x = self.x
        self.assertEqual(complexities[SIN], create_tree(sin(x)).get_complexity())
        self.assertEqual(2 * complexities[SIN], create_tree(sin(2 * x)).get_complexity())

    def test_taskset(self):
        factory = TaskFactory()
        pairs = []
        num = 3
        for name in ['simplify', 'trig']:
            for comp in ['easy', 'medium', 'hard']:
                pairs.append((name, comp))
        tasks = [factory.get(name, comp) for name, comp in pairs]
        taskset = TaskSet(tasks)
        taskset.generate(num=num)
        self.assertEqual(num, len(taskset.taskset))
        for variant in taskset.taskset:
            self.assertEqual(len(pairs), len(variant))


if __name__ == '__main__':
    unittest.main()
