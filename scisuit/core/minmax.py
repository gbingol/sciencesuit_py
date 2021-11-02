from scisuit.core import Vector, Matrix

import numbers

def minmax(entry, axis=None):
      """
      Find the min and max elements <br>

      list: all entries must be real numbers (int/float) <br>
      Matrix: axis=0 or 1, for row or column
      """
      if(isinstance(entry, list)):
            Min = Max = entry[0]

            for i in entry:
                  if(isinstance(i, numbers.Real)==False):
                        raise ValueError("list entries must be real numbers")
                  Min = Min if Min<i else i
                  Max = Max if Max>i else i
                  
            
            return Min, Max
      
      elif(isinstance(entry, Vector)):
            return entry.minmax()

      elif(isinstance(entry, Matrix)):
            
            if(axis==None):
                  return entry.minmax()

            if(isinstance(axis, int)==False):
                  raise TypeError("axis must be of type int")
            
            if(not(axis==0 or axis==1)):
                  raise ValueError("axis must be either 0 or 1")

            return entry.minmax(axis)