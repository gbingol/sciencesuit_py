from __SCISUIT import trapz as __trapz

from scisuit.core import Vector 

import numbers
from typing import Callable

import types



def trapz_d(y, x):
      """
      integrate sampled data using the trapezoidal rule.
      """
      
     
      IsYOK = isinstance(y, list) or isinstance(y, Vector)
      IsXOK = isinstance(x, list) or isinstance(x, Vector)


      if(IsYOK and IsXOK):    
            return __trapz(x,y)
      else:
            raise TypeError("x and y must be of type list/Vector")




def trapz(f:callable, a:float, b:float, inter=100):
      """
      integrate f(x) using the trapezoidal rule.
      """

      if(isinstance(f, types.FunctionType)):
                        
            IsOK = isinstance(a,numbers.Number) and isinstance(b, numbers.Number) and isinstance(inter, int)

            if(IsOK):
                  return __trapz(f, a, b, inter)

      raise TypeError("(f:callable, a:number, b:number, inter:int)") 

