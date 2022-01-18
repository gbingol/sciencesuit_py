import numbers
import types

import scisuit.core as scr

def fsolve(F:list, x0:list, tol=1E-5, maxiter=100 ):
	"""
	F: a list of functions <br>
	x0: a list of initial values <br>

	Solves a system of non-linear equations using Newton's approach
	Funcs contains table of equations in the format of f(x1,x2,...)=0
	v initial starting vector

	USAGE EXAMPLE

	def f1(t): return t[0]**2 + t[1]**2 - 5
	def f2(t): return t[0]**2 - t[1]**2 - 1
	roots, iter=fsolve([f1,f2], [1,1])
	print(roots, "  iter:", iter) 1.73205	1.41421	iter:5
	print(f1(roots), " ", f2(roots)) 9.428e-09    9.377e-09 
	
	"""
	if(not isinstance(F, list)):
		raise TypeError("F must be a list of functions")

	if(not isinstance(x0, list)):
		raise TypeError("a must be a number")

	if(not isinstance(tol, numbers.Number) and tol>0):
		raise TypeError("tol must be a positive number")

	if(not isinstance(maxiter, int) and maxiter>0):
		raise TypeError("maxiter must be a positive integer")

	dimF = len(F)
	dimX0 = len(x0)

	if(dimF<2):
		raise ValueError("At least 2 functions are required")

	if(dimF != dimX0):
		raise ValueError("F and x0 must have same length")

	#instead of using two separate, let's use one as dimF=dimX0
	dim = dimF

	#solution vector
	v = scr.Vector(x0)
      
	#values of each function	
	Fvals = scr.Vector(dim)

	Jacobi = scr.Matrix(dim, dim) 

	for iter in range(maxiter):
		maxfuncval = 0 #convergence criteria
		func= None

	
		for i in range(dim):
			func = F[i]     #function

			if(isinstance(func, types.FunctionType) == False):
				raise ValueError("Entries of F must be functions of form f(t) = 0" ) 
			
			Fvals[i] = func(v.tolist())
                  
		
			for j in range(dim):
				oldval = v[j]
				
				#Note that vector contains (xi+dx,...)
				v[j] += tol  
				
				#evaluate function with (xi+dx,...)
				f_dxi = func(v.tolist()) 
				
				#restore the old value, vector again contains (xi,...)
				v[j] = oldval
				
				#evaluate function with (xi,...)
				f_xi = func(v.tolist())  
				
				if(abs(maxfuncval) < abs(f_xi)): 
					maxfuncval = abs(f_xi) 
				
				#register the derivative with respect to xi to Jacobian matrix
				Jacobi[i, j] = (f_dxi - f_xi) / tol



		#return solution vector (as table) and number of iterations
		if(abs(maxfuncval) < tol): 
			return v.tolist(),  iter

		DetJacobi = abs(scr.det(Jacobi))
            
		if(DetJacobi <= tol):
			raise RuntimeError("At iter="+ str(iter) + " Jacobian Det=" + str(DetJacobi) + ", try different initial values") 
		
		
		v = v - scr.solve(Jacobi, Fvals)