from scisuit.core import Vector, Matrix, sum

from .var import var

import numbers
import math

def kurt(y):
      """
      Computes excess kurtosis. <br>

      y: Vector / list.

      """
      n=len(y)

      if(n < 4):
            raise ValueError("list/Vector must have at least 4 elements")
      
      TypeOK = isinstance(y, list) or isinstance(y, Vector)

      if(TypeOK == False):
            raise TypeError("list/Vector expected")
      
      Total = sum(y)
      avg = Total / n
      stdev = math.sqrt(var(y, ddof=1))

      s=0
      for Num in y:
            if(isinstance(Num, numbers.Number)==False):
                  raise TypeError("entries must be of type number")
            s += (Num - avg)**4
      
      return (s/n)/(stdev)**4 - 3
