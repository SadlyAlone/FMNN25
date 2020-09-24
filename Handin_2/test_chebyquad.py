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
optimization_problem = optimisation_problem_class(chebyquad, gradient=gradchebyquad, h=1e-8)
line_search = exact_line_search(chebyquad, gradchebyquad, tolerance = 1e-10)
regular_newton = regular_newton(optimization_problem, x, 1e-10, line_search)

regular_newton.find_min()
