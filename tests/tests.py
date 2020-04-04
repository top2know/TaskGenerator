import unittest

from app import app
from generator.generators import *
from printer.printing import *


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

    def test_check_generators_roots(self):
        x = self.x
        for i in range(len(self.methods) * (len(self.methods) + 1)):
            ans = x + np.random.randint(-5, 6)
            gen = generator(ans, i, roots=True)
            self.assertNotEqual(ans, gen)
            self.assertEqual(ans, gen.simplify())

    def test_routes(self):
        with app.test_client() as client:
            self.assertEqual('200 OK', client.get('/news').status)
            self.assertEqual('308 PERMANENT REDIRECT', client.get('/tree').status)
            self.assertEqual('200 OK', client.get('/tree/1').status)


if __name__ == '__main__':
    unittest.main()
