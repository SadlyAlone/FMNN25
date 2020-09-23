from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
from .hessian import hessian_approximation
from .problem_class import optimisation_problem_class

class optimisation_method_class:
    """
    This is the base optimization class to be extended by other classes
    takes an optimisation_problem_class which describes the objective function: optimisation_problem_class,
     an initial point: x_0,
     and a convergence tolerance: tolerance
    """
    def __init__(self, optimisation_problem_class, x_0, tolerance):
        self.optimisation_problem_class = optimisation_problem_class
        self.x_0 = x_0
        self.tolerance = tolerance

    """
    This is the method you shold call on the children of this class to find the minimum using
    the specific methods defined in the child class.
    """
    def find_min(self, h=1e-5):
        cond = True
        x = self.x_0
        x_all = []

        while cond:
            x_all.append(x)

            dir = self.search_dir(x, h)
            a = self.line_search_factor(x, h, dir)
            print(x)
            x = x + a*dir

            if la.norm(x - x_all[-1]) < self.tolerance:
                cond = False
        return x_all
    #Method to be inherited by children
    def line_search_factor(self):
        return 1
    #Method to be inherited by children
    def search_dir(self, x):
        return 1

class regular_newton(optimisation_method_class):

    def __init__(self, optimisation_problem_class, x_0, tol):
        optimisation_method_class.__init__(self, optimisation_problem_class, x_0, tol)

    #Calculates the line search factor, maybe take more parameters to decide if we do inexact or exact, or no line search
    def line_search_factor(self, x, h, dir):
        return self.exact_line_search(x, h, dir)
    #Calculates the newton direction using approximation methods contained in hessian.py
    def search_dir(self, x, h):
        gradient = np.array(self.optimisation_problem_class.gradient_approx(x, h))

        hessian = np.array(self.optimisation_problem_class.hessian_approx(x, h))

        return -np.linalg.inv(hessian) @ gradient

    def exact_line_search(self, x, h, dir):

        """
        Exact line search using the bisection method
        In: x is the current point, dir is the search direction
        Out: returnes the stepsize the minimized the search function
        """
        #This is an implementation of the bisection method for exact line search

        #This is the derivative of our F(lambda) = f(x +lambda*dir). The search function is minimized when this is equal to 0.
        search_func = lambda step: (self.optimisation_problem_class.gradient_approx(x +step*dir, h) @ dir)

        #We create an interval starting at the derivative of the current point
        a = search_func(0);
        step_size = 0.01
        b = a
        #Search in the search direction until the sign changes, then the minimum is within
        #this interval, SEEMS LIKE WE SOMETIME SEARCH IN A NON DESCENT DIRECTION WHICH MAKES THIS LOOP RUN ENDLESSLY
        while search_func(a)*search_func(b) > 0:
            step_size = step_size*2
            b = search_func(step_size)

        #Halve the interval until it has reached a certain length

        while abs(b-a) > self.tolerance:
            m = (a + b)/2
            f_m = search_func(m)

            if f_m <= 0:
                a = m
            elif f_m > 0:
                b = m
            else:
                print("Bisection method fails")
                return
        #Return the midpoint of the interval

        return (a+b)/2
