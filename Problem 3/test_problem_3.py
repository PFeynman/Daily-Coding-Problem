import unittest
from problem_3 import Node, serialize, deserialize

class TestsProblem3(unittest.TestCase):
  def test_serialize(self):
    node = Node('root')
    self.assertEqual(serialize(node), 'root null null')
  
  def test_serialize_full_tree(self):
    tree = Node('root', Node('left', Node('left.left'), Node('left.right')), Node('right'))
    self.assertEqual(serialize(tree), 'root left left.left null null left.right null null right null null')
  
  def test_deserialize(self):
    node_str = 'root null null'
    self.assertEqual(serialize(deserialize(node_str)), node_str)

  def test_deserialize_full_tree(self):
    tree_str = 'root left left.left null null null right null null'
    self.assertEqual(serialize(deserialize(tree_str)), tree_str)

  def test_deserialize_node_of_tree(self):
    tree_str = 'root left left.left null null null right null null'
    self.assertEqual(serialize(deserialize(tree_str).left.left), 'left.left null null')

if __name__ == '__main__':
  unittest.main()