from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
from .hessian import hessian_approximation
from .problem_class import optimisation_problem_class

class optimisation_method_class:
    """
    This is the base optimization class to be extended by other classes
    takes an optimisation_problem_class which describes the objective function
    """
    def __init__(self, optimisation_problem_class, x_0, tolerance):
        self.optimisation_problem_class = optimisation_problem_class
        self.x_0 = x_0
        self.tolerance = tolerance

    def find_min(self):
        cond = True
        x = self.x_0
        while cond:
            x_old = x
            #h should not be hardcoded
            h = 0.00001
            dir = self.search_dir(x, h)
            a = self.line_search_factor(x, dir)

            x = x + a*dir

            if la.norm(x - x_old) < self.tolerance:
                cond = False

        return x

    def line_search_factor(self):
        return 1

    def search_dir(self, x):
        return 1

class regular_newton(optimisation_method_class):

    def __init__(self, optimisation_problem_class, x_0, tol):
        optimisation_method_class.__init__(self, optimisation_problem_class, x_0, tol)


    def line_search_factor(self, x, dir):
        return self.exact_line_search(x, dir)

    def search_dir(self, x,h):
        gradient = np.array(self.optimisation_problem_class.gradient(x))
        hessian = np.array(self.optimisation_problem_class.get_hessian(x,h))
        return -np.linalg.inv(hessian) @ gradient

    def exact_line_search(self, x, dir):

        """
        Exact line search using the bisection method
        In: x is the current point, dir is the search direction
        Out: returnes the stepsize the minimized the search function
        """
        #This is an implementation of the bisection method for exact line search
        #Define an interval starting at the search function evaluation at our current x
        #search_func = lambda step: self.optimisation_problem_class(x + step*dir)
        search_func = lambda step: (self.optimisation_problem_class.gradient(x +step*dir) @ dir)

        #print(x + dir)
        #print(self.optimisation_problem_class([2,3]))
        a = search_func(0);
        step_size = 0.1
        b = a
        #Search in the search direction until the sign changes, then the minimum is within
        #this interval

        while sign(a)*sign(b) > 0:
            step_size = step_size*2
            b = search_func(step_size)
        #Halve the interval until it has reached a certain length
        while abs(b-a) > self.tolerance:
            m = (a + b)/2
            if search_func(a)*search_func(m) < 0:
                b = m
            elif search_func(b)*search_func(m) < 0:
                a = m
        #Return the midpoint of the interval

        return (a+b)/2
