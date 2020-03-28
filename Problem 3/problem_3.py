from queue import LifoQueue

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

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

def deserialize(str):
  tree_array = str.rsplit(' ')
  return None