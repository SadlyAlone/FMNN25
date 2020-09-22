from .hessian import hessian_approximation
class optimisation_problem_class:
    def __init__(self, function, gradient=None):
        self.function = function
        self.gradient = gradient
        self.hessian_approx = hessian_approximation(self.function)
    def __call__(self, x):
        return self.function(x)

    def get_hessian(self, x, h):
        return self.hessian_approx(x,h)
