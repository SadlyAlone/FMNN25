import classes

def f(x):
    return x[0]**3 + x[1]**4
    
op = classes.OP_class(f)
x = [2,3]
tol = 0.00001
regular_newton = classes.Regular_newton(op, x, tol)

print(regular_newton.find_min())
