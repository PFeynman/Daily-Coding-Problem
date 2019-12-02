import unittest
from problem_2 import first_approach, second_approach, third_approach

class TestsProblem2(unittest.TestCase):
  def setUp(self):
    self.input_array  = [[1, 2, 3, 4, 5], [3, 2, 1]]
    self.output_array = [[120, 60, 40, 30, 24], [2, 3, 6]]

  def test_first_approach(self):
    for pair in zip(self.input_array, self.output_array):
      self.assertListEqual(first_approach(pair[0]), pair[1])

  def test_second_approach(self):
    for pair in zip(self.input_array, self.output_array):
      self.assertListEqual(second_approach(pair[0]), pair[1])

  def test_third_approach(self):
    for pair in zip(self.input_array, self.output_array):
      self.assertListEqual(third_approach(pair[0]), pair[1])