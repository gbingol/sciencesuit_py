from scisuit.core import Vector, Matrix

def cumsum(entry, axis=None):
      if(isinstance(entry, list)):
            retList=[]
            sum=0

            for i in entry:
                  sum += i
                  retList.append(sum)
            
            return retList
      
      elif(isinstance(entry, Vector)):
            retVec=entry.copy()
            retVec.cumsum()

            return retVec

      elif(isinstance(entry, Matrix)):
            retMat=entry.copy()

            if(axis==None):
                  retMat.cumsum()
                  return retMat

            if(isinstance(axis, int)==False):
                  raise TypeError("axis must be of type int")
            
            if(not(axis==0 or axis==1)):
                  raise ValueError("axis must be either 0 or 1")

            retMat=entry.copy()
            retMat.cumsum(axis)

            return retMat