from scisuit.core import Vector, Matrix

import numbers

def sum(entry, exponent=1.0, axis=None):
      """
      Find the sum for list/Matrix/Vector <br>

      list: all entries must be real numbers (int/float) <br>
      Matrix: axis=0 or 1, for row or column <br>

      <br>

      Ex: v=Vector([1,2,3]) <br>
      sum(v) -> 6, sum(v, exponent=2) ->14


      """

      if(isinstance(exponent, numbers.Real) == False):
            raise TypeError("exponent must be real number")

      if(isinstance(entry, list)):
            retList=[]
            sum=0

            for i in entry:
                  if(isinstance(i, numbers.Real)==False):
                        raise ValueError("list entries must be real numbers")
                  sum += i**exponent
            
            return sum
      
      elif(isinstance(entry, Vector)):
            return entry.sum(exponent)

      elif(isinstance(entry, Matrix)):
            MatCopy=entry.copy()
            MatCopy.pow(exponent)

            if(axis==None):
                  return MatCopy.sum()

            if(isinstance(axis, int)==False):
                  raise TypeError("axis must be of type int")
            
            if(not(axis==0 or axis==1)):
                  raise ValueError("axis must be either 0 or 1")

            return MatCopy.sum(axis)

      else:
            raise TypeError("list/Matrix/Vector expected")