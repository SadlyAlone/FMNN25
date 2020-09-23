from classes.problem_class import optimisation_problem_class
from classes.method_class import optimisation_method_class
from classes.method_class import regular_newton
from classes.hessian import hessian_approximation
import numpy as np
import matplotlib.pyplot as plt

def rosenbrock(x):
    return 100*((x[1] - x[0]*x[0])**2) + (1 - x[0])**2

def rgrad(x):
    return [400*x[0]- 400*x[0]*x[1] + 2*x[0] - 2, 200*(x[1]-x[0]*x[0])]

rosenbrock_lam = lambda x,y: 100*(y-x**2)**2 + (1-x)**2

optimization_problem = optimisation_problem_class(rosenbrock)
#Does not converge for all X due to naive newton implementation.
#Sometimes we cant invert hessian, sometimes search direction is not descent direction
regular_newton = regular_newton(optimization_problem, [2,2], 1e-10)
x_iter = regular_newton.find_min(1e-8)


print(rosenbrock_lam(2,2))

x = [item[0] for item in x_iter]
y = [item[1] for item in x_iter]
start, stop, n_values = -5, 5, 800
x_vals = np.linspace(start, stop, n_values)
y_vals = np.linspace(start, stop, n_values)

X, Y = np.meshgrid(x_vals,y_vals)
Z = rosenbrock_lam(X,Y)

cp = plt.contourf(X, Y, Z)
plt.colorbar(cp)

plt.scatter(x_iter[0][0],x_iter[0][1], marker="s")
plt.scatter(x[-1],y[-1], marker="x")
plt.plot(x,y)

plt.show()
