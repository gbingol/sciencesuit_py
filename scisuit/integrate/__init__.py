import SCISUITSYSTEM

import numbers
from typing import Callable
from scisuit import Vector

import types

def cumtrapz(y, x=None, a=None, b=None, nodes=None, inter=10):
      """
      Cumulatively integrate y(x) using the trapezoidal rule.
      """
      
      #notice that Vector is callable but here we are specifically looking for function (not the general callables)
      if(not isinstance(y, types.FunctionType)):
            IsYOK = isinstance(y, list) or isinstance(y, Vector)
            IsXOK = isinstance(x, list) or isinstance(x, Vector)


            if(IsYOK and IsXOK):    
                  return SCISUITSYSTEM.cumtrapz(x,y)
            else:
                  raise TypeError("x/y must be of type list/Vector")
            
      
      elif(isinstance(y, types.FunctionType)):
            IsNodesOK = isinstance(nodes, list) or isinstance(nodes, Vector)

            if(IsNodesOK):
                  return SCISUITSYSTEM.cumtrapz(y, nodes)
            
            IsOK = isinstance(a,numbers.Number) and isinstance(b, numbers.Number) and isinstance(inter, int)

            if(IsOK):
                  return SCISUITSYSTEM.cumtrapz(y, a, b, inter)

      raise TypeError("Unexpected combination of types.\n"
                  "(y:callable, nodes:list/vector) \n"
                  "(y:callable, a:number, b:number, inter:int) \n"
                  "(x:list/Vector, y:list/Vector)") 





def trapz(y, x=None, a=None, b=None, inter=100):
      """
      integrate y(x) using the trapezoidal rule.
      """
      
      #notice that Vector is callable but here we are specifically looking for function (not the general callables)
      if(not isinstance(y, types.FunctionType)):
            IsYOK = isinstance(y, list) or isinstance(y, Vector)
            IsXOK = isinstance(x, list) or isinstance(x, Vector)


            if(IsYOK and IsXOK):    
                  return SCISUITSYSTEM.trapz(x,y)
            else:
                  raise TypeError("x/y must be of type list/Vector")
            
      
      elif(isinstance(y, types.FunctionType)):
                        
            IsOK = isinstance(a,numbers.Number) and isinstance(b, numbers.Number) and isinstance(inter, int)

            if(IsOK):
                  return SCISUITSYSTEM.trapz(y, a, b, inter)

      raise TypeError("Unexpected combination of types.\n"
                  "(y:callable, a:number, b:number, inter:int) \n"
                  "(x:list/Vector, y:list/Vector)") 




def simpson(y:Callable, a:float, b:float, inter=100)->float:
      """
      Integrate function y(x) using Simpson’s rule.
      """
      if(not isinstance(y, types.FunctionType)):
            raise TypeError("y must be a function")
            
      if(not isinstance(a, numbers.Number)):
            raise TypeError("a must be a number")

      if(not isinstance(b, numbers.Number)):
            raise TypeError("b must be a number")

      if(not isinstance(inter, int)):
            raise TypeError("inter must be an integer")

      return SCISUITSYSTEM.simpson(y, a, b, 100)