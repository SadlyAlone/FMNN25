from classes.problem_class import optimisation_problem_class
from classes.method_class import optimisation_method_class
from classes.method_class import regular_newton
from classes.hessian import hessian_approximation

def g(x):
    return x[0]*x[0] + x[1]*x[1]

optimization_problem = optimisation_problem_class(g)
regular_newton = regular_newton(optimization_problem, [2,3], 0.000001)
print(regular_newton.find_min())
