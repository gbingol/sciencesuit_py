from __SCISUIT import ridder as __ridder

import numbers
from typing import Callable

import types



def ridder(f:callable, a:float, b:float, tol=1E-5, maxiter:int=100 ):
      """
      Finds the root of an equation of form f(x)=0. <br>

      f: A unary function f(x) <br>
      a, b:	The interval where the root lies in  <br>
      tol:	tolerance for error <br>
      maxiter:	Maximum number of iterations during the search for the root 
      """
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(a, numbers.Number)):
            raise TypeError("a must be a number")

      if(not isinstance(b, numbers.Number)):
            raise TypeError("b must be a number")

      if(not isinstance(maxiter, int)):
            raise TypeError("maxiter must be an integer")


      return __ridder(f, a, b, tol, maxiter)