
import numpy as np
import scipy.linalg as la
# import sparse module from SciPy package
from scipy import sparse
from .laplacian_solver import laplacian_solver
# import uniform module to create random numbers
from scipy.stats import uniform
import time
import math



class room:
    def __init__(self, rows, cols, mesh_n):
        self.rows = rows
        self.cols = cols
        self.mesh_n = mesh_n
        self.steps_x = rows*mesh_n
        self.steps_y = cols*mesh_n
        self.boundary = []
        self.condition = ""
        self.v = np.zeros(rows*cols*mesh_n*mesh_n)
        step_size = self.mesh_n



        row = np.array([-4,1]+ (self.steps_x-2)*[0.] + [1] + (self.mesh_n**2 - self.mesh_n - 1)*[0.])
        padding = len(self.v) - len(row)
        row = np.append(row, np.zeros(padding))

        """
        A = la.toeplitz(row)
        D = self.get_D_matrix(A)

        self.A = sparse.csc_matrix(A)
        self.D = sparse.csc_matrix(D)
        """

        self.outer_points = []


    def __call__(self, beyond_points = None):
        v = self.v.reshape(self.steps_y, self.steps_x)
        beyond_points
        v = self.v.reshape(self.steps_y, self.steps_x)
        top = v[0,1:self.steps_x-1]
        left = v[1:self.steps_y-1,0]
        right = v[1:self.steps_y-1,-1]
        bottom = v[-1,1:self.steps_x-1]
        b = np.zeros((self.steps_y-2, self.steps_x-2))
        b[0,:] +=  top
        b[:, 0] +=  left
        b[:, -1] += right
        b[-1, :] += bottom
        if(self.condition=="dirichlet"):
            print(b.flatten())
            print(self.omega(b.flatten()))
            self.v[self.get_inner_points()] = self.omega(b.flatten())

        elif(self.condition=="neumann"):
            b_direction = self.omega.b_direction
            b_new = beyond_points

            if(b_direction=="top"):
                b[0,:] -= top
                b_new -= top
                b_new[0] += v[0,0]
                b_new[-1] += v[0,-1]

                b = np.vstack((b_new, b))
                v_new = self.omega.reconstruct(self.omega(b.flatten()))
                self.v[self.get_inner_points()] = v_new[1:,:].flatten()
                self.v[self.boundary[1:-1]] = v_new[0,:].flatten()

            elif(b_direction=="bottom"):
                b[-1, :] -= bottom
                b_new -= bottom
                b_new[0] += v[-1,0]
                b_new[-1] += v[-1,-1]

                b = np.vstack((b, b_new))
                v_new = self.omega.reconstruct(self.omega(b.flatten()))

                self.v[self.get_inner_points()] = v_new[:-1,:].flatten()
                self.v[self.boundary[1:-1]] = v_new[-1,:].flatten()

            elif(b_direction=="left"):
                b[:, 0] -= left
                b_new -= left
                b_new[0] += v[0,0]
                b_new[-1] += v[-1,0]
                b_new = b_new.reshape(len(b_new),1)


                b = np.hstack((b_new,b))

                v_new = self.omega.reconstruct(self.omega(b.flatten()))
                self.print_v()
                self.v[self.get_inner_points()] = v_new[:,1:].flatten()
                self.v[self.boundary[1:-1]] = v_new[:,1].flatten()
                self.print_v()

            elif(b_direction=="right"):
                b[:, -1] -= right
                b_new -= right
                b_new[0] += v[0,-1]
                b_new[-1] += v[-1,-1]
                b_new = b_new.reshape(len(b_new),1)

                b = np.hstack((b, b_new))
                v_new = self.omega.reconstruct(self.omega(b.flatten()))

                self.v[self.get_inner_points()] = v_new[:,:-1].flatten()
                self.v[self.boundary[1:-1]] = v_new[:,-1].flatten()



    #Indexed from 0
    def set_left(self, row, col, temperature):
        offset = row*self.mesh_n + col*self.steps_x*self.mesh_n
        for i in range(self.mesh_n):
            index = offset + self.steps_x *i
            self.v[index] = temperature
            self.outer_points.append(index)

    def set_right(self, row, col, temperature):
        offset = self.mesh_n -1 + row*self.mesh_n + col*self.steps_x*self.mesh_n
        for i in range(self.mesh_n):
            index = offset + self.steps_x*i
            self.v[index] = temperature
            self.outer_points.append(index)

    def set_top(self, row, col, temperature):
        offset = self.mesh_n*self.steps_x*col + self.mesh_n*row
        for i in range(self.mesh_n):
            index = offset +i
            self.v[index] = temperature
            self.outer_points.append(index)

    def set_bottom(self, row, col, temperature):
        offset = (self.mesh_n-1)*self.steps_x + row*self.mesh_n + col*self.mesh_n*self.steps_x
        for i in range(self.mesh_n):
            index = offset + i
            self.v[index] = temperature
            self.outer_points.append(index)

    def add_room_boundary(self, row, col, side, condition):
        boundary = np.zeros(self.mesh_n)
        if(side=="left"):
            offset = row*self.mesh_n + col*self.steps_x*self.mesh_n
            for i in range(self.mesh_n):
                index = offset + self.steps_x *i
                boundary[i] = index
                self.outer_points.append(index)

        elif(side=="right"):
            offset = self.mesh_n -1 + row*self.mesh_n + col*self.steps_x*self.mesh_n
            for i in range(self.mesh_n):
                index = offset + self.steps_x*i
                boundary[i] = index
                self.outer_points.append(index)


        elif(side=="top"):
            offset = self.mesh_n*self.steps_x*col + self.mesh_n*row
            for i in range(self.mesh_n):
                index = offset + i
                boundary[i] = index
                self.outer_points.append(index)

        elif(side=="bottom"):
            offset = (self.mesh_n-1)*self.steps_x + row*self.mesh_n + col*self.mesh_n*self.steps_x
            for i in range(self.mesh_n):
                index = offset + i
                boundary[i] = index
                self.outer_points.append(index)

        if(condition == "dirichlet"):

            self.omega =  laplacian_solver(self.steps_y-2, self.steps_x-2, condition)
            self.condition = "dirichlet"
        elif(condition == "neumann"):
            self.condition = "neumann"
            if(side == "left" or side == "right"):
                self.omega =  laplacian_solver(self.steps_y-2,self.steps_x-1, condition, side)
            elif(side == "bottom" or side == "top"):
                self.omega =  laplacian_solver(self.steps_y-1,self.steps_x-2, condition, side)
        self.boundary = boundary.astype(int)
    """
    def update_inner(self):
        inner_points = self.get_inner_points()
        A = self.A[inner_points, :]
        self.v[inner_points] = A @ self.v
        return A @ self.v
    """
    def fill_v(self):
        m = np.mean(self.v)
        idx = (self.v == 0)
        self.v[idx] = m

    def coord_to_val(self, x,y):
        return x + y*self.mesh_n*self.cols

    def val_to_coord(self, n):
        x = n % self.mesh_n*self.rows
        y = math.floor(n / self.mesh_n)
        return x,y

    def print_v(self):
        new_v = self.v.reshape(self.steps_y, self.steps_x)
        print(new_v)

    def get_outer_points(self):
        return list(set(self.outer_points))

    def get_inner_points(self):
        return list(set(range(len(self.v))) - set(self.outer_points))
