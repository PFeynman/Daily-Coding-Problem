# My idea made no sense (I wrote it before going to sleep, without thinking a lot). 
# After much thinking, I looked for the solution in geeksforgeeks.org, understood it and implemented it.

def separate(array):
  j = 0
  for i in range(len(array)):
    if array[i] <= 0:
      array[j], array[i] = array[i], array[j]
      j += 1
    
  return j

def find_first_positive(array):
  pivot = separate(array)
  size = len(array) - pivot
  array = array[pivot:]

  for i in range(size): 
    if (abs(array[i]) - 1 < size and array[abs(array[i]) - 1] > 0): 
      array[abs(array[i]) - 1] = -array[abs(array[i]) - 1] 

  for i in range(size): 
    if (array[i] > 0):
      return i + 1

  return size + 1
