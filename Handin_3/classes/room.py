
import numpy as np
import scipy.linalg as la
# import sparse module from SciPy package
from scipy import sparse
# import uniform module to create random numbers
from scipy.stats import uniform
import time



class room:
    def __init__(self, rows, cols, mesh_n):
        self.rows = rows
        self.cols = cols
        self.mesh_n = mesh_n
        self.steps_x = rows*mesh_n
        self.steps_y = cols*mesh_n
        self.boundries = []
        self.v = np.zeros(rows*cols*mesh_n*mesh_n)
        step_size = self.mesh_n

        row = np.array([-4,1]+ (self.steps_x-2)*[0.] + [1] + (self.mesh_n**2 - self.mesh_n - 1)*[0.])
        padding = len(self.v) - len(row)
        row = np.append(row, np.zeros(padding))
        #self.A = la.toeplitz(row)

        self.outer_points = []
        self.A = sparse.csr_matrix(la.toeplitz(row))

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

    def add_room_boundry(self, row, col, side):
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

        self.boundries.append(boundary.astype(int))

    def update_inner(self):
        inner_points = self.get_inner_points()
        A = self.A[inner_points, :]
        self.v[inner_points] = A @ self.v
        return A @ self.v

    def fill_v(self):
        m = np.mean(self.v)
        idx = (self.v == 0)
        self.v[idx] = m

    def coord_to_val(self, x,y):
        return x + y*self.mesh_n*self.cols

    def val_to_coord(self, n):
        x = n % self.mesh_n*self.rows
        y = n % self.mesh_n*self.cols

    def print_v(self):
        new_v = self.v.reshape(self.steps_y, self.steps_x)
        print(new_v)

    def get_outer_points(self):
        return list(set(self.outer_points))

    def get_inner_points(self):
        return list(set(range(len(self.v))) - set(self.outer_points))
