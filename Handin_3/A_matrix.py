# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.sparse import dia_matrix as dia


def george_matrix(n, m, neumann = False):
    """
    Generates the matrix A to solve equation Ax = b with boundary
    
    Note, Hallgrimur prefered "jorge" but after much arguing, george was
    reluctantly settled upon.

    Parameters
    ----------
    n : int
        rows in grid
    m : int
        columns in grid
    neumann : boolean, optional
        whether to use dirichlet or neumann conditions. Note, in current 
        version, presumes neumann condition is on the right of the grid.

    Returns
    -------
    A : sparse matrix (diagonal)

    """
    
    if neumann == True:
        diagonal0 = np.array((([-4.]*(m-1) + [-3.])*n))
    else:
        diagonal0 = -4*np.ones(n*m)
    sub_diagonal = np.array((([1.]*(m-1) + [0.])*n))
    super_diagonal = np.array((([0.]+[1.]*(m-1))*n))
    diagonal2 = np.ones(n*m)
    data = [diagonal2, sub_diagonal, diagonal0, super_diagonal, diagonal2]
    offsets = np.array([-m,-1,0,1,m])
    A = dia((data,offsets),shape=(n*m,n*m))
    return A

#Testing case
# print(george_matrix(3,5, True).todense())



