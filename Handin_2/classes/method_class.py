from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la
from .optimisation_problem_class import optimisation_problem_class

class optimisation_method_class:
    def __init(optimisation_problem_class, x_0, tol):
        self.optimisation_problem_class = optimisation_problem_class
        self.x_0 = x_0
        self.tol = tol

    def find_min():
        cond = False
        x = self.x_0
        x_old = x
        while cond:
            self.x_0 = x_0 + line_search_factor()*search_dir()
            if la.norm(x - x_old) < self.tol:
                cond = True
        return x

    def line_search_factor():
        return 1

    def hessian_dir(x):
        return 1

class regular_newton(optimisation_method_class):

    def __init__(self, optimisation_problem_class, x_0, tol):
        super().__init__(optimisation_problem_class, x_0, tol)

    def line_search_factor():
        return
        #Do SOMETHING HERE
    def search_dir():
        return

        #Do something here

    def exact_line_search(x, dir):

        """
        Exact line search using the bisection method
        In: x is the current point, dir is the search direction
        Out: returnes the stepsize the minimized the search function
        """
        #This is an implementation of the bisection method for exact line search
        #Define an interval starting at the search function evaluation at our current x
        search_func = lambda step: optimisation_problem_class(*(x + step*dir))
        a = search_func(0);
        step_size = 1
        b = a

        #Search in the search direction until the sign changes, then the minimum is within
        #this interval
        while np.sign(a)*np.sign(b) > 0:
            b = search_func(step_size)
            stepSize = stepSize*2

        #Halve the interval until it has reached a certain length
        while abs(b-a) > self.tol:
            m = (a + b)/2
            if search_func(a)*search_func(m) < 0:
                b = m
            elif search_func(b)*search_func(m) < 0:
                a = m
        #Return the midpoint of the interval

        return (a+b)/2
