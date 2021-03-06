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

	if(len(yobs)!=len(factor)):
		raise RuntimeError("yobs and factor have different lengths")
	
	for i in range(len(yobs)):
		sum_x2 += factor[i]**2.0
		sum_xy += factor[i]*yobs[i]
		
	return sum_xy/sum_x2




class linregressResult:
	"""
	Do NOT create an instance of this class directly <br>

	An instance is returned by simple_linregress or multiple_linregress classes' summary methods
	"""
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
		"""standard error"""
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
	def intercept(self):
		"""
		returns dictionary with keys: <br>
		coeff, pvalue, tvalue, SE, CILow, CIHigh
		
		"""
		if(len(self.m_Dict["CoefStats"])>1):
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

	@property
	def coeffstat(self):
		"""
		returns a list containing dictionary with keys: <br>
		coeff, pvalue, tvalue, SE, CILow, CIHigh
		"""
		return self.m_Dict["CoefStats"]





class simple_linregress:
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
			raise TypeError("factor must be of type Vector")



	def compute(self)->list:
		"""
		returns a list containing 
		slope, [intercept] and must be called before summary()
		"""
		self.m_coeffs=None
		if(self.m_intercept):
			Polynom=scr.polyfit(self.m_factor, self.m_yobs, 1)  # an*x^n+...+a0
			self.m_coeffs = Polynom.coeffs()
		else:
			self.m_coeffs = scr.Vector(2)
			self.m_coeffs[0] = FitZeroIntercept(self.m_yobs, self.m_factor)
		
		return self.m_coeffs.tolist()




	def __str__(self) -> str:
		if(len(self.m_coeffs) == 0):
			raise RuntimeError("compute must be called first")

		retStr=""
		if(self.m_intercept):
			retStr += str(self.m_coeffs[0])+"*x + " + str(self.m_coeffs[1])
		else:
			retStr += str(self.m_coeffs[0])+"*x" 
		
		return retStr




	def summary(self):
		if(len(self.m_coeffs) == 0):
			raise RuntimeError("compute must be called first")
		
		N = len(self.m_yobs)

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

		ResultClass = linregressResult(retTable)

		return ResultClass






class multiple_linregress:
	"""
	multiple linear regression
	"""
	def __init__(self, yobs, factor, intercept=True, alpha=0.05) -> None:
		self.m_yobs=yobs
		self.m_factor=factor
		self.m_intercept=intercept
		self.m_alpha=alpha
		
		if(isinstance(yobs, scr.Vector)==False):
			raise TypeError("yobs must be of type Vector")

		if(isinstance(factor, scr.Matrix)==False):
			raise TypeError("factor must be of type Matrix")
		
		if(factor.nrows() != len(yobs)):
			raise ValueError("Number of rows of matrix must be equal to the dimension of the Vector.")



	def compute(self)->list:
		self.m_modifiedMatrix = self.m_factor.copy()

		if(self.m_intercept):
			ones = scr.Vector(self.m_factor.nrows()*[1])
			self.m_modifiedMatrix.insert(ones, pos=0, axis=1)

		self.m_coeffs = scr.solve(a=self.m_modifiedMatrix, b=self.m_yobs)

		return self.m_coeffs.tolist()


	def __str__(self) -> str:
		"""
		returns as a0 + a1*X1 + a2*X2 + ...
		"""
		if(len(self.m_coeffs) == 0):
			raise RuntimeError("compute must be called first")

		retStr=""
		N = len(self.m_coeffs)
		
		if(self.m_intercept):
			retStr += str(self.m_coeffs[0]) + " + "
			
			for i in range(1, N-1):
				retStr += str(self.m_coeffs[i]) + "*x" + str(i) + " + "
			
			retStr += str(self.m_coeffs[N-1]) + "*x" + str(N-1)
		else:
			for i in range(0, N-1):
				retStr += str(self.m_coeffs[i]) + "*x" +str(i+1) + " + "
			
			retStr += str(self.m_coeffs[N-1]) + "*x" +str(N)
		
		return retStr


	def summary(self):
		if(len(self.m_coeffs) == 0):
			raise RuntimeError("compute must be called first")

		nrows = self.m_factor.nrows()
		ncols = self.m_factor.ncols()

		MeanYObs = stat.mean(self.m_yobs)
		ypredicted = scr.Vector(nrows)

		SS_Total, SS_Residual = 0, 0
		sum_y2=0
		for i in range(nrows):
			ypredicted[i] = self.m_modifiedMatrix[i, :]*self.m_coeffs #row vector * col vector = number
			
			SS_Total += (MeanYObs-self.m_yobs[i])**2
			SS_Residual += (self.m_yobs[i]-ypredicted[i])**2
			sum_y2 += self.m_yobs[i]**2
		
		NObservations = nrows
		DF_Regression = ncols
		DF_Residual = NObservations - (DF_Regression + 1)
		if(not self.m_intercept):
			DF_Residual = NObservations - DF_Regression
			SS_Total = sum_y2
		
		DF_Total = DF_Regression + DF_Residual

		SS_Regression = SS_Total - SS_Residual

		R2 = SS_Regression/SS_Total

		MS_Residual = SS_Residual / DF_Residual
		MS_Regression = SS_Regression/DF_Regression

		FValue = MS_Regression/MS_Residual

		pvalue = 1-stat.pf(FValue, DF_Regression, DF_Residual)

		ANOVA = {"SS_Total":SS_Total, "SS_Residual":SS_Residual, "SS_Regression":SS_Regression,
				"DF_Regression":DF_Regression, "DF_Residual":DF_Residual, "MS_Residual":MS_Residual,
				"MS_Regression": MS_Regression, 
				"Fvalue": FValue,
				"pvalue": pvalue}
		
		SEMat = scr.inv(scr.trans(self.m_modifiedMatrix)*self.m_modifiedMatrix)
		SE = scr.sqrt(scr.diag(SEMat))*math.sqrt(MS_Residual)

		CoefStats=[]
		for i in range(len(self.m_coeffs)):
			tbl = {}

			tbl["coeff"] = self.m_coeffs[i]
			tbl["SE"] = SE[i]
			
			Tvalue = self.m_coeffs[i]/SE[i]
			tbl["tvalue"] = Tvalue

			if(Tvalue>=0):
				tbl["pvalue"] = 2*(1-stat.pt(q=Tvalue,df=nrows-1))
			else:
				tbl["pvalue"] = 2*stat.pt(q=Tvalue,df=nrows-1)
			
			
			invTval = stat.qt(self.m_alpha/2.0, DF_Residual)
			
			val1 = self.m_coeffs[i] - SE[i]*invTval
			val2 = self.m_coeffs[i] + SE[i]*invTval

			tbl["CILow"] = min(val1,val2)
			tbl["CIHigh"] = max(val1,val2)

			CoefStats.append(tbl)


		retTable = {"CoefStats":CoefStats, "ANOVA":ANOVA, "R2":R2, "SE":SE}

		return linregressResult(retTable)





def linregress(yobs, factor, intercept=True, alpha=0.05):
	"""
	yobs: Dependent data (vector, list) <br>
	factor: independent data (matrix, 2D list) <br>
	intercept: True if there is intercept <br>
	alpha: significance level
	"""
	Observed = yobs
	Factor = factor

	if(isinstance(yobs, list)):
		Observed = scr.Vector(yobs)

	if(isinstance(factor, list)):
		if(isinstance(factor[0], list)):
			Factor = scr.Matrix(factor) #each list is a row
			Factor = scr.trans(Factor) #each list now is a column
		else:
			Factor = scr.Vector(factor)


	if(isinstance(Factor, scr.Matrix)):
		return multiple_linregress(Observed, Factor, intercept, alpha)
	
	elif(isinstance(Factor, scr.Vector)):
		return simple_linregress(Observed, Factor, intercept, alpha)
	
	else:
		return TypeError("factor must be either list, 2D list, Matrix or Vector")