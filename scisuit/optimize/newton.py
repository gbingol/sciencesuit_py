import SCISUITSYSTEM

import numbers
import types



def secant(f:callable, x0:float, x1:float, tol=1E-5, maxiter:int=100 ):
      """
      Finds the root of an equation of form f(x)=0. <br>

      f: A unary function f(x) <br>
      x0, x1: Initial guesses  <br>
      tol: tolerance for error <br>
      maxiter: Maximum number of iterations  
      """

      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(x0, numbers.Number)):
            raise TypeError("x0 must be a number")

      if(not isinstance(x1, numbers.Number)):
            raise TypeError("x1 must be a number")

      if(not isinstance(tol, numbers.Number) and tol>0):
            raise TypeError("tol must be a number")

      if(not isinstance(maxiter, int) and maxiter>0):
            raise TypeError("maxiter must be a positive integer")


      return SCISUITSYSTEM.secant(f, x0, x1, tol, maxiter)



def newtonraphson(f:callable, x0:float, fprime:callable, tol=1E-5, maxiter:int=100 ):

      """
       Finding root of an equation using Newton-Raphson Method <br>
      
      f: a unary function<br>
      X0: initial guess <br>
      fprime: derivative of f <br>
      tol:	tolerance for error <br>
      maxiter:	Maximum number of iterations
      """
      
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(x0, numbers.Number)):
            raise TypeError("x0 must be a number")

      if(not isinstance(fprime, types.FunctionType)):
            raise TypeError("fprime must be a function")

      if(not isinstance(tol, numbers.Number) and tol>0):
            raise TypeError("tol must be a number")

      if(not isinstance(maxiter, int) and maxiter>0):
            raise TypeError("maxiter must be a positive integer")
            
      
      return SCISUITSYSTEM.newtonraphson(f, x0, fprime, tol, maxiter)



def newton(f:callable, x0:float, x1=None, fprime=None, tol=1E-5, maxiter=100 ):

      """
      Finding root of an equation using Newton-Raphson or Secant Method <br>
      
      f: a unary function<br>
      X0, X1: initial guesses <br>
      fprime: derivative of f <br>
      tol:	tolerance for error <br>
      maxiter:	Maximum number of iterations
      """
      
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(x0, numbers.Number)):
            raise TypeError("x0 must be a number")

      if(not isinstance(tol, numbers.Number) and tol>0):
            raise TypeError("tol must be a number")

      if(not isinstance(maxiter, int) and maxiter>0):
            raise TypeError("maxiter must be a positive integer")
      

      if(fprime == None and x1==None):
            raise TypeError("Either fprime or x1 must be provided")


      if(fprime!=None):
            assert isinstance(fprime, types.FunctionType), "fprime must be a function"

            if(isinstance(x1, numbers.Number)):
                  Warning("Both x1 and fprime provided. fprime taken into account and proceeded with Newton-Raphson method")

            return newtonraphson(f, x0, fprime, tol, maxiter)

      
      if(x1!=None):
            assert isinstance(x1, numbers.Number), "x1 must be a real number"

            return secant(f, x0, x1, tol, maxiter)

          