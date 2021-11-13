import math
import numbers

import scisuit.core as scr
import scisuit.stats as stat



def FitZeroIntercept(yobs, factor):
      """
      Equation to be solved: a1.x=y1, a2.x=y2 ..... an.x=yn

	Best solution: trans(A)*A*x=trans(A)*b	where A is a matrix with first column a's and second column 0s
	trans(A)*A = a1^2+a2^2+...+an^2
	trans(A)*b = a1*b1+a2*b2+...+an*bn
	x = (trans(A)*b) / (trans(A)*A)

      Also note that (important for coefficient analysis)
	var(beta1) = var(sum(xy)/sum(x^2)) = [1/sum(x^2)]^2 * sum(x^2)*var(population)
	sd(beta1) = S(population)/sqrt(sum(x^2))
	
      """
      sum_x2=0
      sum_xy=0
      
      for i in yobs:
            sum_x2 += factor[i]**2
            sum_xy += factor[i]*yobs[i]
            
      return sum_xy/sum_x2




class linregress:
      """
      simple linear model
      """
      
      def __init__(self, yobs, factor, intercept=True, alpha=0.05) -> None:
          self.m_yobs=yobs
          self.m_factor=factor
          self.m_intercept=intercept
          self.m_alpha=alpha
          
          if(isinstance(yobs, scr.Vector)==False):
                raise TypeError("yobs must be of type Vector")
          if(isinstance(factor, scr.Vector)==False):
                raise TypeError("yobs must be of type Vector")

      

      class linregressResult:
            def __init__(self, Dict) -> None:
                self.m_Dict = Dict
            
            @property
            def all(self):
                  """returns the dictionary containing all results"""
                  return self.m_Dict


            @property
            def R2(self):
                  return self.m_Dict["R2"]
            
            @property
            def stderr(self):
                  return self.m_Dict["SE"]

            @property
            def pvalue(self):
                  """
                  p-value from ANOVA stat
                  """
                  return self.m_Dict["ANOVA"]["pvalue"]
            
            
            @property
            def fvalue(self):
                  """
                  F-value from ANOVA statis
                  """
                  return self.m_Dict["ANOVA"]["Fvalue"]
            
            @property
            def slope(self):
                  """
                  returns dictionary with keys: <br>
                  coeff, pvalue, tvalue, SE, CILow, CIHigh
                  
                  """
                  if(len(self.m_Dict["CoefStats"])==2):
                        return self.m_Dict["CoefStats"][1]
                  
                  return self.m_Dict["CoefStats"][0]

            @property
            def intercept(self):
                  """
                  returns dictionary with keys: <br>
                  coeff, pvalue, tvalue, SE, CILow, CIHigh
                  
                  """
                  if(len(self.m_Dict["CoefStats"])==2):
                        return self.m_Dict["CoefStats"][0]
                  
                  return None

            @property
            def ANOVA(self):
                  """
                  returns dictionary with keys: <br>
                  DF_Residual, SS_Residual, MS_Residual, DF_Regression, SS_Regression, MS_Regression <br>
                  SS_Total, Fvalue, pvalue
                  """
                  return self.m_Dict["ANOVA"]



      
      def compute(self):
            """
            returns slope, [intercept] and must be called before summary()
            """
            self.m_coeffs=None
            if(self.m_intercept):
                  Polynom=scr.polyfit(self.m_factor, self.m_yobs, 1)  # an*x^n+...+a0
                  self.m_coeffs = Polynom.coeffs()

                  return self.m_coeffs[0], self.m_coeffs[1]
            else:
                  self.m_coeffs = scr.Vector(2,0)
                  self.m_coeffs[0] = FitZeroIntercept(self.m_yobs, self.m_factor)
            
            return self.m_coeffs[0]

      

      
      def __str__(self) -> str:
          retStr=""
          if(self.m_intercept):
                retStr += str(self.m_coeffs[0])+"*x + " + str(self.m_coeffs[1])
          else:
                retStr += str(self.m_coeffs[0])+"*x" 
            
          return retStr
      



      def summary(self):
            if(len(self.m_coeffs) == 0):
                  raise RuntimeError("compute must be called first")
            
            N=len(self.m_yobs)

            if(N < 2):
                  raise ValueError("At least 3 entries must be provided")
            
            mean_x, mean_y=stat.mean(self.m_factor), stat.mean(self.m_yobs)

            sum_xy, sum_x2, sum_y2, sum_y, sum_x, sum_mean_x, SS_Total=0, 0, 0, 0, 0, 0, 0

            for i in range(N):
                  xi, yi= self.m_factor[i], self.m_yobs[i]
                  sum_x += xi
                  sum_y += yi
                  sum_x2 += xi**2
                  sum_y2 += yi**2
                  sum_xy += xi*yi
                  sum_mean_x += (xi-mean_x)**2
                  SS_Total += (yi-mean_y)**2 #total variability (SS total)

            
            df = N-2
            if(self.m_intercept == False):
                  df = N-1
                  SS_Total=sum_y2
            
            #Forming the ANOVA table for regression
            Polynom=scr.Polynomial(self.m_coeffs)
            fit_y = Polynom.eval(self.m_factor)

            residual=self.m_yobs - fit_y
            residual_2 = residual**2

            SS_Residual=sum(residual_2)
            SS_Regression = SS_Total - SS_Residual

            MS_Regression, MS_Residual=SS_Regression, SS_Residual/df

            ANOVA={"DF_Residual":df, "SS_Residual":SS_Residual, "MS_Residual":MS_Residual,
				"DF_Regression":1, "SS_Regression":SS_Regression, "MS_Regression":MS_Regression, 
				"SS_Total":SS_Total}
            
            ANOVA["Fvalue"] = MS_Regression/MS_Residual
            ANOVA["pvalue"] = 1-stat.pf(ANOVA["Fvalue"], ANOVA["DF_Regression"], ANOVA["DF_Residual"])

            

            def CoeffStat(beta, SE_beta, t_beta):
                  pvalue=0

                  #area on the left of tcrit + area on the right of positive
                  if(t_beta<=0):
                        pvalue = stat.pt(q=t_beta, df=df) + (1-stat.pt(q=abs(t_beta), df=df))
                  
                  #area on the right of positive tcritical + area on the left of negative tcritical
                  elif(t_beta>0):
                        pvalue = (1-stat.pt(q=t_beta, df=df)) + stat.pt(q=-t_beta, df=df) 
                  

                  tbl = {"coeff":beta, "pvalue":pvalue, "tvalue":t_beta, "SE":SE_beta }

                  invTval=stat.qt(self.m_alpha/2.0, ANOVA["DF_Residual"])

                  val1 = beta - SE_beta*invTval
                  val2 = beta + SE_beta*invTval

                  tbl["CILow"] = min(val1,val2)
                  tbl["CIHigh"] = max(val1,val2)

                  return tbl
            
            
            #std error of population
            s=math.sqrt(MS_Residual)

            SE_beta1=s/math.sqrt(sum_mean_x)

            if(not self.m_intercept):
                  SE_beta1 = s/math.sqrt(sum_x2)
            
            beta1, beta0=self.m_coeffs[0], self.m_coeffs[1]

            t_beta1=beta1/SE_beta1

            tbl1 = CoeffStat(beta1, SE_beta1, t_beta1)

            CoefStats=[]

            
            #tbl0
            if(self.m_intercept):
                  SE_beta0 = s*math.sqrt(sum_x2)/(math.sqrt(N)*math.sqrt(sum_mean_x))
                  t_beta0=beta0/SE_beta0
                  
                  tbl0 = CoeffStat(beta0, SE_beta0, t_beta0)

                  CoefStats=[tbl0, tbl1]
            else:
                  CoefStats=[tbl1]

            
            R2=SS_Regression/SS_Total

            retTable={"CoefStats":CoefStats, "ANOVA":ANOVA, "R2":R2, "SE":s}

            ResultClass=linregress.linregressResult(retTable)

            return ResultClass
