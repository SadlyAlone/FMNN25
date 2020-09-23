from classes.problem_class import optimisation_problem_class
from classes.method_class import optimisation_method_class
from classes.method_class import regular_newton
from classes.method_class import david_fletcher_powell
from classes.hessian import hessian_approximation


#Some functions to test the newton method on
def g(x):
    return x[0]*x[0] + x[1]*x[1]
def f(x):
    return
def rosenbrock(x):
    return 100*((x[1] - x[0]*x[0])**2) + (1 - x[0])**2

def rgrad(x):
    return [400*x[0]- 400*x[0]*x[1] + 2*x[0] - 2, 200*(x[1]-x[0]*x[0])]


#optimization_problem = optimisation_problem_class(rosenbrock)
#Does not converge for all X due to naive newton implementation.
#Sometimes we cant invert hessian, sometimes search direction is not descent direction
#regular_newton = regular_newton(optimization_problem, [2,2], 1e-10)
#print(regular_newton.find_min(1e-8))

#optimization_problem = optimisation_problem_class(g)
#DFP = david_fletcher_powell(optimization_problem, [0.3,0.3], 1e-2)
optimization_problem = optimisation_problem_class(rosenbrock)
DFP = david_fletcher_powell(optimization_problem, [0.9,0.9], 1e-10)
print(DFP.find_min(iterations=2))
