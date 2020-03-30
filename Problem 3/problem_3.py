from queue import LifoQueue

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
      return self.val

def serialize(root):
  stack = LifoQueue()
  serialized_tree = str()
  
  stack.put(root)

  while not stack.empty():
    node = stack.get()
    if node is None:
      serialized_tree += 'null '
    else:
      serialized_tree += f'{node.val} '
      stack.put(node.right)
      stack.put(node.left)
  
  return serialized_tree.rstrip()

def deserialize(tree_string: str):
  tree_array = tree_string.split(' ')
  return deserialize_array(tree_array)

def deserialize_array(tree_array):
  val = tree_array.pop(0)
  
  if val == 'null':
    return None
  
  node = Node(val)
  node.left = deserialize_array(tree_array)
  node.right = deserialize_array(tree_array)

  return node