# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:42:38 2020

@author: Heima
"""

import numpy as np
import scipy.linalg as la

def gradient(f,x,h):
    g = []
    for i in range(len(x)):
        e_basis = np.zeros(len(x))
        e_basis[i] = h
        a = (f(x + e_basis) - f(x))/h
        g.append(a)
    return np.asarray(g)


def find_hessian(f,h,x0,tol):
    x_old = x0
    H = np.eye(len(x0))
    g_old = gradient(f,x_old,h)
    s = -H@g_old
    alpha = exact_line_search(x_old, s, 1e-05)
    x_new = x_old + alpha*s
    g_new = gradient(f,x_new,h)
    while la.norm(g_old - g_new) > tol:
        x_old = x_new
        g_old = g_new
        s = -H@g_old
        alpha = exact_line_search(x_old, s, 1e-05)
        x_new = x_old + alpha*s
        g_new = gradient(f,x_new,h)
        delta = x_new - x_old
        gamma = g_new - g_old
        H = H + ((delta - H@gamma)@(H@delta).T)/(H@delta.T @ gamma)
    return H


def test_func(x):
    return (x[1]-x[0]**2)**2 + (1-x[0])**2

x = np.array([1,1])

g = gradient(test_func,x,0.0000000001)
print(g)


H = find_hessian(test_func,0.00001,np.array([1.5,1.5]),np.eye(2),1e-05)




















"""
Test stuff
"""
def f(x):
    return 100*(x[1]-x[0]**2)**2 + (1-x[0])**2

def grad_f(x):
    a = -400*x[0]*(x[1] - x[0]**2) - 2*(1 - x[0])
    b = 200*(x[1] - x[0]**2)
    return np.array([a,b])

x = [2,2]

grad_1 = gradient(f,x,0.00001)
grad_2 = grad_f(x)

print(grad_1)
print(grad_2)