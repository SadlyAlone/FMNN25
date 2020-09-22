from .hessian import hessian_approximation
class optimisation_problem_class:
    def __init__(self, function, gradient=None):
        self.function = function
        self.hessian_approximation = hessian_approximation(self.function)
        self.gradient = gradient
    #Evaluates the objective function at given point x
    def __call__(self, x):
        return self.function(x)

    #Approximates the gradient at x, where h is small number used to approximate derivative
    #If gradient was given, instead evaluates directly
    def gradient_approx(self, x, h):

        if self.gradient == None:
            return self.hessian_approximation.gradient(self.function, x, h)
        else:
            return self.gradient(x)
    #Approximates the hessian at x, where h is small number used to approximate derivative
    def hessian_approx(self, x, h=0.00001):
        return self.hessian_approximation(x,h)
