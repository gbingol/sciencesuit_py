import cmath

from __SCISUIT import muller_x012 as __muller_x012
from __SCISUIT import muller_x0 as __muller_x0

import numbers
from typing import Callable


def muller(f:callable, x0, h=None, x1=None, x2=None, tol=1E-5, maxiter=100):
    """
    
    """
    #In all cases f and x0 must be provided
    if(not isinstance(f, Callable)):
        raise TypeError("f must be callable")
    
    if(not (isinstance(x0, complex) or isinstance(x0, numbers.Number))):
        raise TypeError("x0 must be either complex or real number")

    if(not isinstance(tol, float) or tol<=0):
        raise TypeError("tol must be float greater than zero")

    if(not isinstance(maxiter, int) or maxiter<=0):
        raise TypeError("maxiter must be int greater than zero")

    
    #if x1 and x2 provided, then no need for h
    if(x1 != None and x2 != None):
        if(not (isinstance(x1, complex) or isinstance(x1, numbers.Number))):
            raise TypeError("x1 must be either complex or real number")
        
        if(not (isinstance(x2, complex) or isinstance(x2, numbers.Number))):
            raise TypeError("x2 must be either complex or real number")
        
        if(h!=None):
            Warning("if x1 and x2 are provided, h will not be taken into account")
        
        return __muller_x012(f, x0, x1, x2, tol, maxiter)


    if(h==None):
        h=0.5

    if(not (isinstance(h, complex) or isinstance(h, numbers.Number))):
        raise TypeError("h must be either complex or real number")

    if(x1!=None or x2!=None):
        Warning("When (x1 or x2) and h is defined, h will be taken into account")

    return __muller_x0(f, x0, h, tol, maxiter)

    
