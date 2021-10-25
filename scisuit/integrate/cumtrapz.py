import SCISUITSYSTEM

import numbers
from typing import Callable

import types




def cumtrapz_d(y, x):
      """
      Cumulatively integrate sampled data.
      """
      
     
      IsYOK = isinstance(y, list) or isinstance(y, Vector)
      IsXOK = isinstance(x, list) or isinstance(x, Vector)


      if(IsYOK and IsXOK):    
            return SCISUITSYSTEM.cumtrapz(x,y)
      else:
            raise TypeError("x and y must be of type list/Vector")





def cumtrapz(f:callable, a=None, b=None, nodes=None, inter=10):
      """
      Cumulatively integrate f(x) using the trapezoidal rule.
      """
      
     
      if(isinstance(f, types.FunctionType)):
            IsNodesOK = isinstance(nodes, list) or isinstance(nodes, Vector)

            if(IsNodesOK):
                  return SCISUITSYSTEM.cumtrapz(f, nodes)
            
            IsOK = isinstance(a,numbers.Number) and isinstance(b, numbers.Number) and isinstance(inter, int)

            if(IsOK):
                  return SCISUITSYSTEM.cumtrapz(f, a, b, inter)

      raise TypeError("Unexpected combination of types.\n"
                  "(f:callable, nodes:list/vector) \n"
                  "(f:callable, a:number, b:number, inter:int)") 

