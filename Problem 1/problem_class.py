class Problem:
  
  def __init__(self, k, numberList):
    self.k = k
    self.numberList = numberList

  def setK(self, k):
    self.k = k
  
  def setNumberList(self, newList):
    self.numberList = newList
  
  def findSumToK(self):
    for i in range(0, len(self.numberList)):
      for j in range(i, len(self.numberList)):
        if self.k == self.numberList[i] + self.numberList[j]:
          return True

    return False
  
  def findSumToKOnePass(self):
    numbers_seen = set()
    for number in self.numberList:
      if self.k - number in numbers_seen:
        return True
      else:
        numbers_seen.add(number)

    return False

def main():
  _problem = Problem(17, [10, 15, 3, 7])
  print(_problem.findSumToK)
  print(_problem.findSumToKOnePass)

if __name__ == "__main__":
  main()