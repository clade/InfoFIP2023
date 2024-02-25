import math

from .base import Function


class MathFunction(Function):
    def display(self, *args):
        return '{}({})'.format(self.function_name,self.args[0].display())


class Sin(MathFunction):     
    function_name = 'sin'
    math_function = math.sin
    partial_derivative = (lambda x:cos(x),)


class Cos(MathFunction):     
    function_name = 'cos'
    math_function = math.cos
    partial_derivative = (lambda x:-sin(x),)


sin = Sin
cos = Cos
