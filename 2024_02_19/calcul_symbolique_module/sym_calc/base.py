import numbers
import operator
import math

class Expr(object):

    def binary_operator(self, other, operator):
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(other, Expr):
            return operator(self, other)
        return NotImplemented

    def reversed_binary_operator(self, other, operator):
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(other, Expr):
            return operator(other, self)
        return NotImplemented

    def __add__(self, other):
        return self.binary_operator(other, Sum)
        
    def __mul__(self, other):
        return self.binary_operator(other, Prod)

    def __truediv__(self, other):
        return self.binary_operator(other, Div)

    def __sub__(self, other):
        return self.binary_operator(other, Sub)

    def __radd__(self, other):
        return self.reversed_binary_operator(other, Sum)
 
    def __rmul__(self, other):
        return self.reversed_binary_operator(other, Prod)

    def __rtruediv__(self, other):
        return self.reversed_binary_operator(other, Div)

    def __rsub__(self, other):
        return self.reversed_binary_operator(other, Sub)

    def __neg__(self):
        return Neg(self)
    
    def __repr__(self):
        return self.display()

    def diff(self, var):
        out = self._diff(var)
        return out.simplify()
    
    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        lhs = self.simplify()
        rhs = other.simplify()
        if not type(lhs)==type(rhs):
            return False
        return lhs.is_equal_to(rhs)


class Node(Expr):
    pass

class Leave(Expr):
    def simplify(self):
        return self

class Symbol(Leave):
    def __init__(self, symbole):
        self.symb = symbole
        
    def display(self, *args):
        return self.symb
    
    def evaluate(self, **kwd):
        try:
            return kwd[self.symb]
        except KeyError:
            raise Exception(f"La valeur de {self.symb!r} n'est pas définie")

    def is_equal_to(self, other):
        return self.symb==other.symb

    def _diff(self, var):
        if self==var:
            return Number(1)
        return Number(0)

class Number(Leave):
    def __init__(self, nombre):
        if not isinstance(nombre, numbers.Number):
            raise ValueError
        self.nbre = nombre
        
    def display(self, *args):
        return str(self.nbre)
    
    def evaluate(self, **kwd):
        return self.nbre

    def is_equal_to(self, other):
        return other.nbre==self.nbre
        
    def _diff(self, var):
        return Number(0)

class Function(Node):
    """ Function with an arbitrary number of arguments """
    def __init__(self, *args):
        self.args = args

    def evaluate(self, **kwd):
        evaluated_args = [elm.evaluate(**kwd) for elm in self.args]
        return self.math_function(*evaluated_args)

    def is_equal_to(self, other):
        if not type(self)==type(other):
            return False        
        return self.args==other.args

    def _diff(self, var):
        partial_derivative = getattr(self, 'partial_derivative', None)
        if partial_derivative is None:
            raise NotImplementedError(f'Cannot derivate function {self.__class__}')
        if len(self.args)==0:
            return Number(0)
        out = self.args[0].diff(var)*partial_derivative[0](*self.args)
        for deriv, arg in zip(partial_derivative[1:], self.args[1:]):
            out = out + arg.diff(var)*deriv(*self.args)
        return out

    liste_simplification = []
    def simplify(self):
        out = type(self)(*[elm.simplify() for elm in self.args])
        for elm in self.liste_simplification:
            tmp = getattr(out, elm)()
            if tmp is not None:
                return tmp.simplify()
        return out


class BinaryOperator(Function):
    commutative=False
    def display(self, parent_priority=0):
        if parent_priority>self.priority:
            fmt_str = '({} {} {})'
        else:
            fmt_str = '{} {} {}'
        return fmt_str.format(self.args[0].display(self.priority), 
                self.operator_name, self.args[1].display(self.priority))

    def is_equal_to(self, other):
        if not type(self)==type(other):
            return False
        if self.args==other.args:
            return True
        if self.commutative:
            return self.args==other.args[::-1]
        return False

class Sum(BinaryOperator):
    priority = 0
    operator_name = '+'
    math_function=operator.add
    commutative=True    
    partial_derivative = (lambda x, y:1, lambda x, y:1)


    def simplication_de_deux_nombres(self):
        if isinstance(self.args[0], Number) and isinstance(self.args[1], Number):
            return Number(self.args[0].nbre + self.args[1].nbre)

    def simplication_addition_avec_zero(self):
        if self.args[0]==0:
            return self.args[1]
        if self.args[1]==0:
            return self.args[0]

    def simplification_identique(self):
        if self.args[1]==self.args[0]:
            return 2*self.args[0]

    liste_simplification = ['simplication_de_deux_nombres',
        'simplication_addition_avec_zero', 'simplification_identique']

class Prod(BinaryOperator):
    priority = 1
    operator_name = '*'
    math_function=operator.mul
    commutative=True    
    partial_derivative = (lambda x, y:y, lambda x, y:x)

    def simplication_de_deux_nombres(self):
        if isinstance(self.args[0], Number) and isinstance(self.args[1], Number):
            return Number(self.args[0].nbre * self.args[1].nbre)


    def simplication_multiplication_avec_un(self):
        if self.args[0]==1:
            return self.args[1]
        if self.args[1]==1:
            return self.args[0]

    def simplication_multiplication_avec_zero(self):
        if self.args[0]==0:
            return Number(0)
        if self.args[1]==0:
            return Number(0)

        
    liste_simplification = ['simplication_de_deux_nombres',
        'simplication_multiplication_avec_un', 'simplication_multiplication_avec_zero']


class Div(BinaryOperator):
    priority = 2
    operator_name = '/'
    math_function=operator.truediv
    partial_derivative = (lambda x, y:1/y, lambda x, y:-x/(y*y))


class Sub(BinaryOperator):
    priority = 0.5
    operator_name = '-'
    math_function=operator.sub
    partial_derivative = (lambda x, y:1, lambda x, y:-1)


class UnitaryOperator(Function):
    
    def display(self, parent_priority=0):
        if parent_priority>self.priority:
            fmt_str = '({}{})'
        else:
            fmt_str = '{}{}'
        return fmt_str.format(self.unitary_symbol, 
                              self.args[0].display(self.priority))
            
class Neg(UnitaryOperator):
    priority = 0.5
    unitary_symbol = "-"
    math_function = operator.neg
    partial_derivative = (lambda x:-1,)


    

def simplify(expr):
    return expr.simplify()

if __name__=="__main__":
    x = Symbol('x')