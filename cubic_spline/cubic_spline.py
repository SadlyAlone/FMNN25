from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

class cubic_spline:
  def __init__(self, grid, ctrl_points):
    #Multiplicity of grid points
    grid = np.insert(grid, 0, grid[0])
    grid = np.insert(grid, 0, grid[0])
    grid = np.append(grid, grid[-1])
    grid = np.append(grid, grid[-1])
    self.grid = grid

    #Multiplicity of control points
    ctrl_points = np.vstack((ctrl_points[0], ctrl_points))
    ctrl_points = np.vstack((ctrl_points[0], ctrl_points))
    ctrl_points = np.vstack((ctrl_points, ctrl_points[-1]))
    ctrl_points = np.vstack((ctrl_points, ctrl_points[-1]))
    self.ctrl_points = ctrl_points

    self.s_list = []


  def __call__(self, u):
    """
    Calls the Blossom algorithm.
    In: parameter value u.
    Out: spline value s(u)
    """
    #Find i, for grid point u_i left of u
    idx = self.find_hot_interval(u)
    #Make an array containing the non-zero control points for parameter u
    rec_list = np.array(self.ctrl_points[idx-2:idx+2])

    #Call recursive blossom algorithm
    return self.blossom_recursion(rec_list, u, idx)


  def create_spline_list(self, n=51,
               print_parameter_values = False,
               print_spline_values = False):
    """
    Updates the list of spline values according to a given amount of
    data points n. Optionally prints this list or the list of parameter values.
    """
    #Create list between u_2 and u_(max-2) with n elements
    u_list = np.linspace(self.grid[2], self.grid[-3], n)
    #Calculate spline for every value in list
    self.s_list = [self(u_list[i]) for i in range(len(u_list))]

    #Optional, prints parameter and spline data
    if (print_parameter_values):
      print(u_list)
    if (print_spline_values):
      print(self.s_list)


  def find_hot_interval(self, u):
    """
    Searches for the "hot" interval containing u
    In: parameter value u.
    Out: for interval u_(i) to u_(i+1) containing u, returns index i.
    """
    if u == self.grid[-1]:
      return len(self.grid) - 4
    else:
      index = np.argmax(self.grid > u)
      return index - 1


  def blossom_recursion(self, rec_list, u, idx):
    """
    Defines the recursive blossom algorithm.
    In: parameter value u, non-zero control points rec_list, index idx
    Out: if recursion is complete, return the spline value s(u), otherwise,
    calculate the next step of the blossom algorithm
    and call this function recursively.
    """
    #Determine how many values remain
    list_length = len(rec_list)

    #If only one value remains, recursion is complete
    if list_length == 1:
      return [rec_list[0,0], rec_list[0,1]]
    #Otherwise, define the left-most index in each step
    else:
      left_step = -list_length + 2
    #Right-most index is always 1.
    right_step = 1

    #Loop to update each value in the rec_list
    for k in range(list_length - 1):
      #Determine correct grid points by summing position in rec_list, idx and
      #left/right_step.
      u_left  = self.grid[k + idx + left_step]
      u_right = self.grid[k + idx + right_step]
      #Calculate scale factor alpha
      alpha = (u_right - u)/(u_right - u_left)
      #Run blossom algorithm
      rec_list[k] = alpha*rec_list[k] + (1-alpha)*rec_list[k+1]

    #Discard last value in rec_list
    rec_list = rec_list[0:list_length-1]
    #Run recursion for new rec_list
    return self.blossom_recursion(rec_list, u, idx)


  def make_basis_function(self, idx):
    """
    Calls the basis_fun for degree 3 and returns a polynomial basis function.
    """
    return self.basis_fun(idx, 3)


  def step_fun(self, u, idx):
    """
    The zero-th basis function of the splines.
    In: parameter value u and index idx
    Out: 1 if u is within interval of index I to I+1
    """
    grid = self.grid#[2:-3]
    #Return zero if grid points coincide
    if grid[idx-1] == grid[idx]:
      return 0
    #Check if u is contained within chosen interval
    elif u >= grid[idx-1] and u < grid[idx]:
      return 1
    else:
      return 0


  def basis_fun(self, idx, k):
    """
    Recursively generates basis functions of polynomial degree k, using basis
    functions of degree k-1 (or, if k-1=0, the step function).
    In: index idx and polynomial degree k
    Out: basis function N(u)
    """
    grid = self.grid#[2:-3]
    #Call step function for last step of recursion
    if k == 0:
      return lambda u: self.step_fun(u, idx)
    else:
      #Handle cases when grid points coincide
      if grid[idx + k - 1] == grid[idx - 1]:
        f1 = lambda u: 0
      else:
        f1 = lambda u: (u - grid[idx - 1])/(grid[idx + k - 1] - grid[idx - 1])
      #First recursion step
      N1 = lambda u: self.basis_fun(idx, k-1)(u)

      if idx + k == len(grid) or grid[idx + k] == grid[idx]:
        f2 = lambda u: 0
      else:
        f2 = lambda u: (grid[idx + k] - u)/(grid[idx + k] - grid[idx])
      if idx + k == len(grid):
        N2 = lambda u: 0
      else:
        N2 = lambda u: self.basis_fun(idx+1, k-1)(u)

      #Returns a polynomial of degree k
      return lambda u: f1(u)*N1(u) + f2(u)*N2(u)

  def basis_spline(self, u):
    """
    Evaluates the spline using basis functions and control points, rather than
    blossoms.
    In: parameter value u
    Out: spline value s(u)
    """
    #Initialise
    sum = 0
    #Find index
    idx = self.find_hot_interval(u)

    #Sum non-zero basis functions with control points
    for k in range(idx-2, idx+2):
      sum += self.ctrl_points[k]*self.make_basis_function(k)(u)
    return sum



  def plot_spline(self, n = 51, control_polygon = False):
    """
    Plots the the spline that the class spits out.
    In: n determines how many points the plot has.
    Out: plots the spline.
    Written by: Halli
    """
    self.create_spline_list(n)

    x,y = zip(*self.s_list)
    plt.plot(x,y,'b')

    if (control_polygon):
      ctrl_x, ctrl_y = zip(*self.ctrl_points)
      plt.scatter(ctrl_x,ctrl_y,c='r')
      plt.plot(ctrl_x,ctrl_y,'r--')
