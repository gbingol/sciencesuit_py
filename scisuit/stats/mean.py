from scisuit.core import Vector, Matrix, sum

import numbers

def mean(entry, exponent=1.0, axis=None):
      """
      Find the mean for list/Matrix/Vector <br>

      list: all entries must be real numbers (int/float) <br>
      Matrix: axis=0 or 1, for row or column <br>

      <br>

      Ex: v=Vector([1,2,3]) <br>
      sum(v) -> 6, sum(v, exponent=2) ->14


      """

      if(isinstance(exponent, numbers.Real) == False):
            raise TypeError("exponent must be real number")

      if(isinstance(entry, list)):
            Total=sum(entry, exponent)
            
            return Total/len(entry)
      
      elif(isinstance(entry, Vector)):
            return entry.sum(exponent)/len(entry)

      elif(isinstance(entry, Matrix)):
            MatCopy=entry.copy()
            MatCopy.pow(exponent)

            if(axis==None):
                  return MatCopy.sum()/len(MatCopy)

            if(isinstance(axis, int)==False):
                  raise TypeError("axis must be of type int")
            
            if(not(axis==0 or axis==1)):
                  raise ValueError("axis must be either 0 or 1")

            Len= MatCopy.nrows() if axis==0 else MatCopy.ncols()

            V=MatCopy.sum(axis)
            return V/Len

      else:
            raise TypeError("list/Matrix/Vector expected")