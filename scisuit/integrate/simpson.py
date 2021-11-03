from __SCISUIT import simpson as __simpson

import numbers
from typing import Callable

import types



def simpson(f:Callable, a:float, b:float, inter=100)->float:
      """
      Integrate function f(x) using Simpson’s rule.
      """
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(a, numbers.Number)):
            raise TypeError("a must be a number")

      if(not isinstance(b, numbers.Number)):
            raise TypeError("b must be a number")

      if(not isinstance(inter, int)):
            raise TypeError("inter must be an integer")

      return __simpson(f, a, b, 100)