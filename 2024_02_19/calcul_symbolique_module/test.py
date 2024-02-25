import unittest

from sym_calc import *


class TestSymCal(unittest.TestCase):
    def test_eval(self):
        x = Symbol('x')
        y = Symbol('y')

        expr1 = x + y
        self.assertEqual(expr1.evaluate(x=1, y=2), 3)

    def test_diff(self):
        x = Symbol('x')
        y = Symbol('y')

        expr1 = x + sin(2*y)

        self.assertEqual(expr1.diff(x), 1)
        self.assertEqual(expr1.diff(y), 2*cos(2*y))

        
    def test_comm(self):
        x = Symbol('x')
        y = Symbol('y')

        self.assertEqual(x+y, y+x)
        
        
if __name__=='__main__':
    unittest.main()