from scisuit.core import Vector, Matrix

def var(y, ddof=0, axis=None):
    TypeOK=isinstance(y, list) or isinstance(y, Vector) or isinstance(y, Matrix)
    if(TypeOK == False):
        raise TypeError("list / vector / Matrix expected")
    
    AxisValOK = axis==None or axis==0 or axis==1
    if(AxisValOK == False):
        raise ValueError("axis must be 0 or 1")
    
    if(isinstance(y, Matrix)):
        return y.var(axis=axis, ddof=ddof)
    
    if(isinstance(y, Vector)):
        return y.var(ddof)
    
    v=Vector(y)
    return v.var(ddof)