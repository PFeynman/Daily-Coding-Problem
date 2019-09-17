import unittest
from problem_class import Problem

class TestsProblem1(unittest.TestCase):

  def setUp(self):
    self.problem = Problem(17, [10, 15, 3, 7])

  def test_K_is_defined(self):
    self.assertIsInstance(self.problem.k, int)
  
  def test_list_of_numbers_is_defined(self):
    self.assertIsInstance(self.problem.numberList, list)

  def test_set_k_value(self):
    n = 17
    self.problem.setK(n)
    self.assertEqual(n, self.problem.k)

  def test_set_list_number_values(self):
    newValues = [10, 15, 3, 7]
    self.problem.setNumberList(newValues)
    self.assertListEqual(newValues, self.problem.numberList)
  
  def test_numbers_add_up_to_k(self):
    n = 17
    self.problem.setK(n)
    newValues = [10, 15, 3, 7]
    self.problem.setNumberList(newValues)
    self.assertTrue(self.problem.findSumToK())

  def test_numbers_add_up_to_k_one_pass(self):
    n = 17
    self.problem.setK(n)
    newValues = [10, 15, 3, 7]
    self.problem.setNumberList(newValues)
    self.assertTrue(self.problem.findSumToKOnePass())