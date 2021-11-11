from scisuit.core import Vector, Matrix, sum

from .var import var

import numbers
import math

def kurt(v):
      """
      Computes excess kurtosis. <br>

      v: Vector / list.

      """
      n=len(v)

      if(n < 4):
            raise ValueError("list/Vector must have at least 4 elements")
      
      TypeOK = isinstance(v, list) or isinstance(v, Vector)

      if(TypeOK == False):
            raise TypeError("list/Vector expected")
      
      Total = sum(v)
      avg = Total / n
      stdev = math.sqrt(var(v, 1))

      s=0
      for Num in v:
            s += ((Num - avg)/stdev)**4
      
      return s*n*(n+1)/((n-1)*(n-2)*(n-3)) - 3*(n-1)**2/((n-2)*(n-3))
