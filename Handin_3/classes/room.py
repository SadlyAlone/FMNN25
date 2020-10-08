
import numpy as np


class room:
    def __init__(self, rows, cols, mesh_n):
        self.rows = rows
        self.cols = cols
        self.mesh_n = mesh_n
        self.steps_x = rows*mesh_n
        self.steps_y = cols*mesh_n
        self.boundries = []
        self.v = np.zeros(rows*cols*mesh_n*mesh_n)

    #Indexed from 0
    def set_left(self, row, col, temperature):
        offset = row*self.mesh_n + col*self.steps_x*self.mesh_n
        for i in range(self.mesh_n):
            self.v[offset + self.steps_x *i] = temperature

    def set_right(self, row, col, temperature):
        offset = self.mesh_n -1 + row*self.mesh_n + col*self.steps_x*self.mesh_n
        for i in range(self.mesh_n):
            self.v[offset + self.steps_x*i] = temperature

    def set_top(self, row, col, temperature):
        offset = self.mesh_n*self.steps_x*col + self.mesh_n*row
        for i in range(self.mesh_n):
            self.v[offset + i] = temperature

    def set_bottom(self, row, col, temperature):
        offset = (self.mesh_n-1)*self.steps_x + row*self.mesh_n + col*self.mesh_n*self.steps_x
        for i in range(self.mesh_n):
            self.v[offset + i] = temperature

    def set_room_boundry(self, row, col, dir):
        boundary = np.zeros(self.mesh_n)
        if(dir=="left"):
            offset = row*self.mesh_n + col*self.steps_x*self.mesh_n
            for i in range(self.mesh_n):
                boundary[i] = offset + self.steps_x *i

        elif(dir=="right"):
            offset = self.mesh_n -1 + row*self.mesh_n + col*self.steps_x*self.mesh_n
            for i in range(self.mesh_n):
                boundary[i] = offset + self.steps_x*i

        elif(dir=="top"):
            offset = self.mesh_n*self.steps_x*col + self.mesh_n*row
            for i in range(self.mesh_n):
                boundary[i] = offset + i

        elif(dir=="bottom"):
            offset = (self.mesh_n-1)*self.steps_x + row*self.mesh_n + col*self.mesh_n*self.steps_x
            for i in range(self.mesh_n):
                boundary[i] = offset + i

        self.boundries.append(boundary)

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
