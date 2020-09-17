from classes.OP_class import OP_class
from classes.opt_method_class import opt_method_class
f = lambda x,y: x^2 + y^2
op = OP_class(f)
regular_newton = regular_newton(op)
