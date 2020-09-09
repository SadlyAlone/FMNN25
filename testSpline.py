import unittest
import cubic_spline
import numpy as np

class TestSpline(unittest.TestCase):
  CONTROL = [(-12.73564, 9.03455),
  (-26.77725, 15.89208),
  (-42.12487, 20.57261),
  (-15.34799, 4.57169),
  (-31.72987, 6.85753),
  (-49.14568, 6.85754),
  (-38.09753, -1e-05),
  (-67.92234, -11.10268),
  (-89.47453, -33.30804),
  (-21.44344, -22.31416),
  (-32.16513, -53.33632),
  (-32.16511, -93.06657),
  (-2e-05, -39.83887),
  (10.72167, -70.86103),
  (32.16511, -93.06658),
  (21.55219, -22.31397),
  (51.377, -33.47106),
  (89.47453, -33.47131),
  (15.89191, 0.00025),
  (30.9676, 1.95954),
  (45.22709, 5.87789),
  (14.36797, 3.91883),
  (27.59321, 9.68786),
  (39.67575, 17.30712)]
  grid = np.linspace(0,1,26)
  spline = cubic_spline.cubic_spline(grid, CONTROL)

  def test_init(self):
    spline = cubic_spline.cubic_spline(self.grid, self.CONTROL)

    assert(all(spline.grid[2:-2] == self.grid))
    assert((spline.ctrl_points[2:-2] == self.CONTROL).all().all())

  def test_multiplicity(self):
    spline = cubic_spline.cubic_spline(self.grid, self.CONTROL)

    assert(spline.grid[0] == spline.grid[1] == spline.grid[2])
    assert(spline.grid[-1] == spline.grid[-2] == spline.grid[-3])

    assert((spline.ctrl_points[0] == spline.ctrl_points[1]).all())
    assert((spline.ctrl_points[1] == spline.ctrl_points[2]).all())

    assert((spline.ctrl_points[-1] == spline.ctrl_points[-2]).all())
    assert((spline.ctrl_points[-2] == spline.ctrl_points[-3]).all())


  def test_blossom(self):
    spline = cubic_spline.cubic_spline(self.grid, self.CONTROL)
    est_points = spline(0.2)
    correct_point = [-31.90219167, 6.47655833]
    self.assertAlmostEqual(est_points[0], correct_point[0])
    self.assertAlmostEqual(est_points[1], correct_point[1])

  def test_deBoor_equal_to_Blossom(self):
    spline = cubic_spline.cubic_spline(self.grid, self.CONTROL)
    u = np.linspace(0,1,101)

    for val in u:
      A = spline(val)
      B = spline.basis_spline(val)
      self.assertAlmostEqual(A[0], B[0])
      self.assertAlmostEqual(A[1], B[1])

  def test_unity_basis(self):
    spline = cubic_spline.cubic_spline(self.grid, self.CONTROL)
    u = np.linspace(0,1,101)

    for val in u:
      idx = spline.find_hot_interval(val)
      sum = 0;
      for i in range(idx-2, idx+2):
        sum += spline.make_basis_function(i)(val)
      self.assertAlmostEqual(sum, 1)


if __name__ =='__main__' :
  unittest.main()
