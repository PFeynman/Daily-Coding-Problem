def first_approach(inList):
  length = len(inList)
  outList = [1] * length
  
  for i in range(0, length):
    for j in range(0, length):
      if i != j:
        outList[j] = outList[j] * inList[i]
        
  return outList

def second_approach(inList):
  length = len(inList)
  outList = [1] * length

  for i in range(0, length):
    for j in range(0, length):
      outList[j] = outList[j] * inList[i]
  
  for i in range(0, length):
    outList[i] = outList[i] / inList[i]
        
  return outList

def third_approach(inList):
  length = len(inList)
  outList = [1] * length
  left = [1] * length
  right = [1] * length

  for i in range(1, length):
    left[i] = inList[i - 1] * left[i - 1]

  for i in range(length - 2, -1, -1):
    right[i] = inList[i + 1] * right[i + 1]

  for i in range(length):
    outList[i] = left[i] * right[i]

  return outList