from scisuit.core import Vector, sum
from scisuit.stats import pf



class aov:
      def __init__(self, *args) -> None:
          self.m_args = args
          self.m_Averages = []
          self.m_SampleSizes = []

          self.m_MSError=None
          self.m_DFTreatment=None
          self.m_DFError=None

      def compute(self):

            SS_Treatment, SS_Error, SS_Total=0, 0, 0
            
            NEntries = 0

            #C is a variable defined to speed up computations (see Larsen Marx Chapter 12 on ANOVA)
            C = 0
            
           
            
            for elem in self.m_args:
                  TypeOK=isinstance(elem, list) or isinstance(elem, Vector)
                  if(TypeOK == False):
                        raise TypeError("list/Vector expected")
                  

                  ElemSize = len(elem)
                  LocalSum=0
                  
                  for entry in elem:
                        LocalSum += entry
                        SS_Total += entry**2
                  
                  #Required for Tukey test
                  self.m_Averages.append(LocalSum/ElemSize)
                  self.m_SampleSizes.append(ElemSize) 

                  C += LocalSum
                  
                  NEntries += ElemSize

                  SS_Treatment = SS_Treatment + LocalSum**2/ElemSize

            
            C = C**2 / NEntries
            
            SS_Total = SS_Total - C
            SS_Treatment = SS_Treatment - C
            SS_Error = SS_Total - SS_Treatment

            self.m_DFError, self.m_DFTreatment= NEntries-len(self.m_args), len(self.m_args)-1 
            DF_Total = self.m_DFError + self.m_DFTreatment

            MS_Treatment, self.m_MSError = SS_Treatment/self.m_DFTreatment , SS_Error/self.m_DFError

            Fvalue = MS_Treatment/self.m_MSError

            pvalue = 1 - pf(q = Fvalue, df1 = self.m_DFTreatment, df2 = self.m_DFError)

            return pvalue