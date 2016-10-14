from location import Location
from datetime import datetime
class Sorts():
    def __init__(self, refObj=None):
        self.refObj = refObj
        
    def mergeSort(self, x):
        start = datetime.now()
        result = []
        if len(x) <= 2:
            return x
            
        mid = int(len(x) / 2)
        y = self.mergeSort(x[:mid])
        z = self.mergeSort(x[mid:])
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i].compareTo(z[j], self.refObj) > 0:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        print datetime.now() - start
        return result
        
        