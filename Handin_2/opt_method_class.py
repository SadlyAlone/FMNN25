from numpy import linalg as LA
class opt_method_class:
    def __init(OP_class, x_0, tol):
        self.OP_class = OP_class
        self.x_0 = x_0
        self.tol = tol

    def find_min():
        cond = False
        x = self.x_0
        x_old = x
        while cond

            self.x_0 = x_0 + line_search_factor()*search_dir();

            if LA.norm(x - x_old) < self.tol:
                cond = True

    def line_search_factor():
        return 1

    def hessian_dir():
        return 1

class regular_newton(opt_method_class):
    def __init__(self, OP_class, x_0, tol):
        super().__init__(OP_class, x_0, tol)

    def line_search_factor():
        #Do SOMETHING HERE
    def search_dir():
        #Do something here
