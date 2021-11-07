import math
import numbers

from scisuit.core import Vector, sum
from scisuit.stats import pf

from ..misc import qdist

class aov:

      class TukeyComparison:
            def __init__(self) -> None:
                self.m_a=None
                self.m_b=None
                self.m_MeanValueDiff=None
                self.m_CILow=None
                self.m_CIHigh=None

            def __str__(self) -> str:
                retStr = str(self.m_a) + "-" + str(self.m_b) + \
                  "\t \t" + \
                  str(round(self.m_MeanValueDiff, 2)) + \
                  "\t \t" + \
                  str(round(self.m_CILow, 2)) + \
                  "," \
                  + str(round(self.m_CIHigh, 2))
                return retStr


      def __init__(self, *args) -> None:
          self.m_args = args
          self.m_Averages = []
          self.m_SampleSizes = []

          self.m_MSError=None
          self.m_DFTreatment=None
          self.m_DFError=None
          self.m_TukeyTable=[]
          self.m_pvalue = None

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

            self.m_pvalue = 1 - pf(q = Fvalue, df1 = self.m_DFTreatment, df2 = self.m_DFError)

            return self.m_pvalue

      
      def tukey(self, Alpha):
            """
            perform tukey test <br>

            tukey(Alpha)-> list
            """
            if(len(self.m_Averages) == 0):
                  raise RuntimeError("first compute must be called")
            
            if(isinstance(Alpha, numbers.Number) == False):
                  raise TypeError("Alpha must be of type number")

            D = qdist.getqdist(1-Alpha, self.m_DFTreatment + 1, self.m_DFError) / math.sqrt(self.m_SampleSizes[0])
            ConfIntervalLength = D*math.sqrt(self.m_MSError)

            self.m_TukeyTable=[]
            for i in range(len(self.m_Averages)):
                  for j in range(i+1, len(self.m_Averages)):
                        
                        MeanValueDiff = self.m_Averages[i]-self.m_Averages[j]
                        ConfInterval1 = MeanValueDiff-ConfIntervalLength
                        ConfInterval2 = MeanValueDiff+ConfIntervalLength

                        com = self.TukeyComparison()

                        com.m_a=i
                        com.m_b=j
                        com.m_MeanValueDiff=MeanValueDiff
                        com.m_CILow=min(ConfInterval1,ConfInterval2)
                        com.m_CIHigh=max(ConfInterval1,ConfInterval2)

                        self.m_TukeyTable.append(com)

            return self.m_TukeyTable
      
      def __str__(self) -> str:
            if(isinstance(self.m_pvalue, numbers.Number) == False):
                  raise RuntimeError("compute method has not been called")
            
            retStr= "p-value = " + str(self.m_pvalue) + "\n"

            retStr += "Pairs \t \t Diff  \t \t Tukey Interval"
            retStr +="\n"
            
            for Entry in self.m_TukeyTable:
                  retStr += str(Entry)
                  retStr += "\n"
            
            return retStr
