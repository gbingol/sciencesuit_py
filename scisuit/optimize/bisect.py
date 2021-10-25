import SCISUITSYSTEM

import numbers
from typing import Callable

import types

def bisect(f:callable, a:float, b:float, tol=1E-5, maxiter:int=100 , method:str="bf", modified:bool=False):
      """
      Finds the root of an equation of form f(x)=0. <br>

      f: A unary function f(x) <br>
      a, b:	The interval where the root lies in  <br>
      tol:	tolerance for error <br>
      maxiter:	Maximum number of iterations during the search for the root <br>
      method:	"bf" for brute-force (halving) <br>
                  "rf" for regula falsi (false position) <br>
      modified:	True for modified regula falsi method. 

      """
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(a, numbers.Number)):
            raise TypeError("a must be a number")

      if(not isinstance(b, numbers.Number)):
            raise TypeError("b must be a number")

      if(not isinstance(maxiter, int)):
            raise TypeError("maxiter must be an integer")

      if(not isinstance(method, str)):
            raise TypeError("method must be string \"bf\" or \"rf\"")

      if(not isinstance(modified, bool)):
            raise TypeError("modified must be bool, True for modified regula falsi")


      return SCISUITSYSTEM.bisect(f, a, b, tol, maxiter, method, modified)