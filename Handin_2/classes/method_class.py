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
            print(x)

            dir = self.search_dir(x, h)
            a = self.line_search_factor(x, h, dir)

            x = self.update_x(x, h)

            if la.norm(x - x_all[-1]) < self.tolerance:
                cond = False
        return x_all
    #Method to be inherited by children
    def update_x(self, x, h):

        dir = self.search_dir(x, h)
        a = self.line_search_factor(x, h, dir)

        return x + a*dir
    def line_search_factor(self):
        return 1
    #Method to be inherited by children
    def search_dir(self, x):
        return 1
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

"""
This is the DFP optimization algorith that extends the general optimisation_method_class
Unfortunatly I had to update the find_min method since the iteration step is not the same
"""
class david_fletcher_powell(optimisation_method_class):

    def __init__(self, optimisation_problem_class, x_0, tol):
        optimisation_method_class.__init__(self, optimisation_problem_class, x_0, tol)
        self.D = np.identity(len(x_0))

    #We have to overrite the find_min function to contain the second loop
    #h is for estimating derivatives (close to 0 relative to the scale of the function)
    #iterations is the number of times you want to run the second iteration loop.
    def find_min(self, iterations=2, h=1e-5, ):
        cond = True
        x = self.x_0
        x_all = []

        while cond:
            x_all.append(x)
            print(x)
            x = self.update_x(x, h, iterations)

            if la.norm(x - x_all[-1]) < self.tolerance:
                cond = False
        return x_all

    def update_x(self, x, h, iterations):
        self.D = np.identity(len(x))
        y = x
        for i in range(iterations):
            d_i = self.search_dir(y, h)
            a = self.line_search_factor(y, h, d_i)


            y_old = y
            y = y + a*d_i
            self.update_D(y, y_old, h)
        return y


    #Calculates the line search factor, maybe take more parameters to decide if we do inexact or exact, or no line search
    def line_search_factor(self, x, h, dir):
        return self.exact_line_search(x, h, dir)
    #Calculates the newton direction using approximation methods contained in hessian.py
    def search_dir(self, x, h):
        gradient = np.array(self.optimisation_problem_class.gradient_approx(x, h))
        return -self.D @ gradient

    #This method updates the matrix D in each step of the inner loop of the DFP algorithm
    def update_D(self, y, y_old, h):

        p = np.array(np.subtract(y, y_old))

        q = np.array(self.optimisation_problem_class.gradient_approx(y, h)) - \
            np.array(self.optimisation_problem_class.gradient_approx(y_old, h))

        first_term = 1/(p @ q)*(p @ p)

        second_term_first = 1 / (q @ self.D @ q)

        second_term_second = self.D @ q @ q

        second_term_final = second_term_first*second_term_second*self.D

        self.D = self.D + first_term - second_term_final


        return
class broyden_fletcher_goldfarb_shanno(optimisation_method_class):

    def __init__(self, optimisation_problem_class, x_0, tol):
        optimisation_method_class.__init__(self, optimisation_problem_class, x_0, tol)
        self.D = np.identity(len(x_0))

    #We have to overrite the find_min function to contain the second loop
    #h is for estimating derivatives (close to 0 relative to the scale of the function)
    #iterations is the number of times you want to run the second iteration loop.
    def find_min(self, iterations=2, h=1e-5, ):
        cond = True
        x = self.x_0
        x_all = []
        while cond:
            x_all.append(x)
            print(x)
            x = self.update_x(x, h, iterations)

            if la.norm(x - x_all[-1]) < self.tolerance:
                cond = False
        return x_all

    def update_x(self, x, h, iterations):
        self.D = np.identity(len(x))
        y = x
        for i in range(iterations):
            d_i = self.search_dir(y, h)
            a = self.line_search_factor(y, h, d_i)
            y_old = y
            y = y + a*d_i
            self.update_D(y, y_old, h)
        return y


    #Calculates the line search factor, maybe take more parameters to decide if we do inexact or exact, or no line search
    def line_search_factor(self, x, h, dir):
        return self.exact_line_search(x, h, dir)
    #Calculates the newton direction using approximation methods contained in hessian.py
    def search_dir(self, x, h):
        gradient = np.array(self.optimisation_problem_class.gradient_approx(x, h))
        return -self.D @ gradient

    #This method updates the matrix D in each step of the inner loop of the DFP algorithm
    def update_D(self, y, y_old, h):

        p = np.array(np.subtract(y, y_old))

        q = np.array(self.optimisation_problem_class.gradient_approx(y, h)) - \
            np.array(self.optimisation_problem_class.gradient_approx(y_old, h))
        first_term_first = (1 + (q @ self.D @ q)/(p @ q)
        first_term_second = 
        first_term = 1/(p @ q)*(p @ p)

        second_term_first = 1 / (q @ self.D @ q)

        second_term_second = self.D @ q @ q

        second_term_final = second_term_first*second_term_second*self.D

        self.D = self.D + first_term - second_term_final


        return
