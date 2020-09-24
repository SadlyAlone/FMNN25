from classes.problem_class import optimisation_problem_class
from classes.method_class import optimisation_method_class
from classes.method_class import regular_newton
from classes.method_class import david_fletcher_powell
from classes.method_class import good_broyden
from classes.method_class import bad_broyden
from classes.method_class import symmetric_broyden
from classes.method_class import broyden_fletcher_goldfarb_shanno
from classes.hessian import hessian_approximation
from classes.inexact_line_search import inexact_line_search
from classes.exact_line_search import exact_line_search
from chebyquad_problem import *

x=linspace(0,1,8)
optimization_problem = optimisation_problem_class(chebyquad, gradient=gradchebyquad)
line_search = exact_line_search(chebyquad, gradchebyquad, tolerance = 1e-10)
regular_newton = regular_newton(optimization_problem, x, 1e-6, line_search)

x_opt = regular_newton.find_min()[-1]

x=linspace(0,1,8)
xmin= so.fmin_bfgs(chebyquad,x,gradchebyquad)  # should converge after 18 iterations
print("This is our methods result")
print(x_opt)
print("This is scipy's results")
print(xmin)
print("This is the difference")
print(xmin - x_opt)
