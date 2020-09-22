from classes import *

f = lambda x,y: x**2 + y**2
f_rosenbrock = lambda x,y: 100*(y - x**2)**2 + (1 - x)**2

op = optimisation_problem_class(f)
regular_newton = regular_newton(op)
