import unittest

from problem_4 import find_first_positive

class TestsProblem4(unittest.TestCase):
  def setUp(self):
    self.input_array  = [[3, 4, -1, 1], [1, 2, 0], [-1, 5, 2, -4, 1, 4, 3]]
    self.output_array = [2, 3, 6]
  
  def test_find_first_positive(self):
    for pair in zip(self.input_array, self.output_array):
      self.assertEqual(find_first_positive(pair[0]), pair[1])

if __name__ == "__main__":
    unittest.main()