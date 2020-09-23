from classes.problem_class import optimisation_problem_class
from classes.method_class import optimisation_method_class
from classes.method_class import regular_newton
from classes.method_class import david_fletcher_powell
from classes.hessian import hessian_approximation
from classes.method_class import good_broyden


#Some functions to test the newton method on
def g(x):
    return x[0]*x[0] + x[1]*x[1]
def f(x):
    return
def rosenbrock(x):
    return 100*((x[1] - x[0]*x[0])**2) + (1 - x[0])**2

def rgrad(x):
    return [400*x[0]- 400*x[0]*x[1] + 2*x[0] - 2, 200*(x[1]-x[0]*x[0])]

def test_func(x):
    return x[0]**3 + x[0]*x[1] + (x[0]**2)*(x[1]**2) - 3*x[0]


#optimization_problem = optimisation_problem_class(rosenbrock)
#Does not converge for all X due to naive newton implementation.
#Sometimes we cant invert hessian, sometimes search direction is not descent direction
print('Here we use the regular newton with exact line search on the rosenbrock function, x_0 = [2,2]')
input('Press enter to continue')
optimization_problem = optimisation_problem_class(rosenbrock)
regular_newton = regular_newton(optimization_problem, [2,2], 1e-10)
regular_newton.find_min(1e-8)

#optimization_problem = optimisation_problem_class(g)
#DFP = david_fletcher_powell(optimization_problem, [0.3,0.3], 1e-2)

#DFP = david_fletcher_powell(optimization_problem, [1.5,1.5], 1e-5)
#print(DFP.find_min(iterations=2,h=1e-5)[-1])
print('Here we use the good broyden with exact line search on f = x^3 + x*y +(x^2)*(y^2) - 3y, (x,y) = [1.1,-0.6]')
input('Press enter to continue')
optimization_problem = optimisation_problem_class(test_func)

GB = good_broyden(optimization_problem, [1.1, -.6], 1e-3)
print(GB.find_min(h=1e-2)[-1])
