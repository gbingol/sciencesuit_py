import numbers
import types

from scisuit import Vector, Matrix

def fsolve(f:callable, x0:list, tol=1E-5, maxiter=100 ):
      """
      Solves a system of non-linear equations using Newton's approach
	Funcs contains table of equations in the format of f(x1,x2,...)=0
	
      f: function(list)
      x0: initial values
	
      """
      if(not isinstance(f, types.FunctionType)):
            raise TypeError("f must be a function")
            
      if(not isinstance(x0, list)):
            raise TypeError("a must be a number")

      if(not isinstance(tol, numbers.Number) and tol>0):
            raise TypeError("tol must be a positive number")

      if(not isinstance(maxiter, int) and maxiter>0):
            raise TypeError("maxiter must be a positive integer")


      dim = len(x0)
      
      F = Vector(dim)
      
      Jacobi = Matrix(dim, dim) 