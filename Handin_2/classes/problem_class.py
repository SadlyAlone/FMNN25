class optimisation_problem_class:
    def __init__(self, function, gradient=None):
        self.function = function
        self.gradient = gradient
    def __call__(self, x):
        return self.function(x)
