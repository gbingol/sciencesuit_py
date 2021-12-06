
import math
import numbers


class Food:
      pass


# component can be water, CHO...; T is temperature in Celcius 
def Cp(component:str, T:float)->float:
	if(component=="water" ):
		return 4.1289 - 9.0864E-05*T + (5.4731*10**-6.0)*T**2 
	
	elif(component=="protein"):
		return 2.0082 + (1.2089*10**-3.0)*T - 1.3129*(10.0**-6.0)*T**2.0 
		
	elif(component=="lipid"):
		return 1.9842 + (1.4733*10.0**-3.0)*T - 4.8008*(10.0**-6.0)*T**2.0
		
	elif(component=="CHO"):
		return 1.5488 + (1.9625*10.0**-3.0)*T - (5.9399*10.0**-6.0)*T**2.0
		
	elif(component=="ash"):
		return 1.0926 + (1.8896*10.0**-3.0)*T - (3.6817*10.0**-6.0)*T**2.0 
	
	elif (component == "salt"):   #Engineering Toolbox
		return 0.88
	
	else:
	      raise Exception("Component must be water, lipid, protein, CHO, ash or salt")





#T in celcius, result W/mK
def ThermConduct (component:str, T:float)->float:
	if(component=="water"): 
		return 4.57109E-01 + (1.7625E-03)*T - (6.7036E-06)*T**2.0 
	
	elif(component=="protein"): 
		return 1.7881E-01 + (1.1958E-03)*T - (2.7178E-06)*T**2.0 
		
	elif(component=="lipid"): 
		return 1.8071E-01-2.7604E-04*T-1.7749E-07*T**2.0 
		
	elif(component=="CHO"):
		return 2.0141E-01+1.3874E-03*T-4.3312E-06*T**2.0 
		 
	elif(component=="ash"): 
		return 3.2962E-01+1.4011E-03*T-2.9069E-06*T**2.0 
		
	elif (component == "salt"): 
		#5.704 molal solution at 20C, Riedel L. (1962),
            # Thermal Conductivities of Aqueous Solutions of Strong Electrolytes Chem.-1ng.-Technik., 23 (3) P.59 - 64
		return 0.574 

	else:
		raise Exception("Component must be water, lipid, protein, CHO, ash or salt")




# T celcius, result kg/m3
def Rho(component:str, T:float)->float:
	if(component=="water"): 
		return 997.18 + (3.1439E-03)*T - (3.7574E-03)*T**2.0 
		
	elif(component=="protein"): 
		return 1329.9 - (5.1840E-01)*T 
		 
	elif(component=="lipid"): 
		return 925.59 - (4.1757E-01)*T 
		
	elif(component=="CHO"): 
		return 1599.1 - (3.1046E-01)*T 
	
	elif(component=="ash"): 
		return 2423.8 - (2.8063E-01)*T 
		
	elif (component == "salt"): 
            #Wikipedia
		return 2165 

	else:
		raise Exception("Component must be water, lipid, protein, CHO, ash or salt")





def Norrish(food:Food)->float:
	# Norrish equation
	
	#CHO is considered as fructose
	NCHO = food.m_CHO/180.16 
	
	#lipid is considered as glycerol
	NLipid = food.m_Lipid/ 92.0944 
	
	#protein is considered as alanine
	NProtein = food.m_Protein/89.09 
	
	NWater = food.m_Water/18.02

	Nsolute=NCHO + NLipid + NProtein

	# Norrish equation K values using Ferro-Chirife-Boquet equation
	K=NCHO/Nsolute*(-2.15) + NLipid/Nsolute*(-1.16) + NProtein/Nsolute*(-2.52) 
	
	# Mole fraction of solute
	XSolute = Nsolute/(Nsolute+NWater) 

	# Mole fraction of water
	XWater=NWater/(Nsolute+NWater) 
	

	return XWater*math.exp(K*XSolute**2)



#mostly used in confectionaries
def MoneyBorn(confectionary:Food)->float:
	# amount of CHO in 100 g water (equation considers thus way) 
	WeightCHO = 100*confectionary.m_CHO/confectionary.m_Water 
	
	#CHO is considered as fructose
	NCHO = WeightCHO/180.16 
	

	return 1.0/(1.0+0.27*NCHO)




def ComputeAw(food:Food)->float:

	#if no matching conditon is found return water activity as 0.92
	retVal=0.92
	
	water:float = food.m_Water #%
	CHO:float = food.m_CHO #%
	lipid:float = food.m_Lipid #%
	protein:float = food.m_Protein #%
	ash:float = food.m_Ash #%
	salt:float = food.m_Salt #%

	Msolute=CHO + lipid + protein + ash + salt



	#There is virtually (<1E-5 %) no water
	if(math.isclose(water,0.0, abs_tol=1E-5)):
		return 0.01 
	

	
	# Dilute solution, as the total percentage is less than 1% 
	# therefore "most likely" very high water activity
	if(Msolute<1): 
		return 0.99 
	
	
	
	#Non-electrolytes solutions
	if(math.isclose(salt, 0.0, abs_tol=1E-5)):
		if(water>99.0):
			return 0.98
		
		#almost all CHO
		elif(water<1.0 and protein<1.0 and lipid<1.0 and ash<1.0 and CHO>98.0): 
			return 0.70
		
		#most likely a candy
		elif(lipid<1.0 and protein<1.0 and ash<1.0 and water>1.0 and water<5.0 and CHO>5.0): 
			retVal=MoneyBorn(food)
		
		elif(water>5.0 and CHO>5.0):
			retVal=Norrish(food)
		

	
	
	T:float = food.m_Temperature

	Cp_20 = water/100.0*Cp("water",20.0) + protein/100.0*Cp("protein",20.0) + \
		lipid/100*Cp("lipid",20.0) +CHO/100*Cp("CHO",20.0) + \
		ash/100.0*Cp("ash",20.0)+salt/100.0*Cp("salt",20.0)

	Cp_T=water/100*Cp("water",T) + protein/100*Cp("protein",T) + \
		lipid/100*Cp("lipid",T) + CHO/100*Cp("CHO",T) + \
		ash/100*Cp("ash",T) + salt/100*Cp("salt",T)

	Cp_avg = (Cp_20 + Cp_T) / 2.0	

	Qs = Cp_avg*(T-20.0) #kJ/kg

	MWavg=water/100*18.02 + CHO/100*180.16 + lipid/100*92.0944 + protein/100*89.09 + salt/100*58.44
	
	Ravg=8.314/MWavg #kPa*m^3/kgK
	
	aw2 = retVal*math.exp(Qs/Ravg*(1/293.15 - 1/(T+273.15)))

	#raise exception
	assert aw2>=0 and aw2<=1,"Water activity is beyond range [0,1]"
	
	
	return aw2
	





class Food:
	"""
	A class to compute thermal and physical properties of food materials
	"""
	
	def __init__(self, **kwargs):
		#Percentages
		self.m_Water = 0.0
		self.m_CHO = 0.0
		self.m_Protein = 0.0
		self.m_Lipid = 0.0
		self.m_Ash = 0.0
		self.m_Salt = 0.0

		self.m_Ingredients={}
		
		for k, value in kwargs.items():
			key= k.lower()

			if(key=="water"): self.m_Water= value
			elif(key=="cho"): self.m_CHO=value
			elif(key=="protein"): self.m_Protein=value
			elif(key=="lipid" or key=="oil" or key=="fat"): self.m_Lipid=value
			elif(key=="ash"): self.m_Ash=value
			elif(key=="salt"): self.m_Salt=value
			else: 
				raise Exception("Keys are CHO, Protein, Lipid(Fat, Oil), Ash, Water, Salt")

		
		#User does not necessarily create a food material where percentage sum is 100
		#Therefore it needs an adjustment where total percentage is ALWAYS 100
		PercentageSum=self.m_Ash + self.m_Lipid + self.m_Protein + self.m_CHO + self.m_Water + self.m_Salt

		self.m_Water = self.m_Water/PercentageSum*100
		self.m_CHO = self.m_CHO/PercentageSum*100
		self.m_Protein = self.m_Protein/PercentageSum*100
		self.m_Lipid = self.m_Lipid/PercentageSum*100
		self.m_Ash = self.m_Ash/PercentageSum*100
		self.m_Salt = self.m_Salt/PercentageSum*100


		self.m_Ingredients["water"]=self.m_Water
		self.m_Ingredients["cho"]=self.m_CHO
		self.m_Ingredients["protein"]=self.m_Protein
		self.m_Ingredients["lipid"]=self.m_Lipid
		self.m_Ingredients["ash"]=self.m_Ash
		self.m_Ingredients["salt"]=self.m_Salt
		

		#Initial values
		self.m_ph=6.0 #No internal function provided for calculation
	
		#In the following cases an internal function is provided, 
		#however, user is allowed to provide a function or a value
		#When that is the case, use the values provided by user. Therefore, __m_aw_userdef variable is defined
		self.m_aw=0.92
		
		self.m_k=0.45
		
		self.m_rho=990
		
		self.m_cp=3.80
		
		self.m_Temperature=20.0 # C
		self.m_Weight=1.0 #Unit weight
		
			
	def __add__(self, rhs):
		return self.x + rhs.x


	def __getitem__(self, index):
		return index
	


	def cp(self, arg=None)->float:
		if(arg == None):
			T = self.m_Temperature
			return (self.m_Water/100)*Cp("water",T) + \
				(self.m_Protein/100)*Cp("protein",T) + \
				(self.m_Lipid/100)*Cp("lipid",T) + \
				(self.m_CHO/100)*Cp("CHO",T) + \
				(self.m_Ash/100)*Cp("ash",T) +  \
				(self.m_Salt/100)*Cp("salt",T)
	
		
		
		elif(callable(arg)):
			
			retVal:float = arg(self)
			
			assert isinstance(retVal, numbers.Number) and retVal>0, "The provided function must return a number value greater than zero."
			
			self.m_cp=retVal

			return retVal
		
		else:
			raise Exception("The args to the function must be either a None or a function")



	#return W/mK
	def k(self, arg=None)->float:
		if(arg==None):
			T=self.m_Temperature

			return (self.m_Water/100)*ThermConduct("water",T)+ \
				(self.m_Protein/100)*ThermConduct("protein",T) + \
				(self.m_Lipid/100)*ThermConduct("lipid",T) + \
				(self.m_CHO/100)*ThermConduct("CHO",T) + \
				(self.m_Ash/100)*ThermConduct("ash",T) + \
				(self.m_Salt/100)*ThermConduct("salt",T)	
			
		elif(callable(arg)):
			retVal=arg(self)
			
			assert isinstance(retVal, numbers.Number) and retVal>0, "Function must return a number value >0."
			
			self.m_k=retVal

			return retVal
		
		else:
			raise Exception("The args to the function can be either a None or a function")




	
	def rho(self, arg=None)->float:
		"""density, return kg/m3"""
		if(arg==None):
			T=self.m_Temperature

			return (self.m_Water/100)*Rho("water",T) + \
				(self.m_Protein/100)*Rho("protein",T) + \
				(self.m_Lipid/100)*Rho("lipid",T) + \
				(self.m_CHO/100)*Rho("CHO",T) + \
				(self.m_Ash/100)*Rho("ash",T) + \
				(self.m_Salt/100)*Rho("salt",T)
		
			
		elif(callable(arg)):
			retVal=arg(self)
			
			assert isinstance(retVal, numbers.Number) and retVal>0, "Function must return a number >0."
			
			self.m_rho=retVal

			return retVal
		
		else:
			raise Exception("The arguments to the function can be either None or a function")





	def aw(self, func=None)->float:
		"""water activity"""
		if(func == None):
			return ComputeAw(self)
			
		elif(callable(func)):
			retVal=func(self)
			
			assert isinstance(retVal, numbers.Number), "Function must return a number value."

			if(retVal<0 or retVal>1):
				raise ValueError("Function must return a water activity in the range of (0,1].")
			
			self.m_aw=retVal
			
			return retVal
		
		else:
			raise Exception("The arguments to the function can be either None or a function")

	



	#Not implemented, however needed for Food safety ops and the thermal processing app
	def ph(self, func=None)->float:

		"""returns pH, notice that this will always return 6.0 unless a function provided"""
		
		if(func==None):
			return self.m_ph
			
		elif(callable(func)):
			retVal=func(self)
			
			assert isinstance(retVal, numbers.Number), "The provided function must return a number value."

			if(retVal<0 or retVal>14):
				raise ValueError("The provided function must return a pH in the range of (0,14).")
			
			self.m_ph=retVal

			return retVal
		
		else:
			raise Exception("The args to the function can be either a nil value, a number or a function")




	@property
	def temperature(self):
		"""
		in Celcius
		"""
		pass

	@temperature.setter
	def temperature(self, T):
		self.m_Temperature = T


	@temperature.getter
	def temperature(self)->float:
		return self.m_Temperature



	@property
	def weight(self):
		"""
		unit weight, NOT recommended to set the weight externally
		"""
		pass


	@weight.setter
	def weight(self, weight:float):
		self.m_Weight=weight
	
	
	@weight.getter
	def weight(self)->float:
		return self.m_Weight


	def normalize(self):
		self.m_Weight = 1.0



	@property
	def Water(self)->float:
		return self.m_Water

	
	@property
	def CHO(self)->float:
		return self.m_CHO


	@property
	def Lipid(self)->float:
		return self.m_Lipid


	@property
	def Protein(self)->float:
		return self.m_Protein


	@property
	def Ash(self)->float:
		return self.m_Ash


	@property
	def Salt(self)->float:
		return self.m_Salt



	def getIngredients(self)->dict:
		return self.m_Ingredients
	



	#similar to mixing of two food items
	def __add__(self, foodB:Food)->Food:
		ma, mb = self.weight,  foodB.weight
		Ta, Tb = self.temperature, foodB.temperature 
		cpa, cpb = self.cp(), foodB.cp()

		water:float = ma*self.Water + mb*foodB.Water
		CHO:float = ma*self.CHO + mb*foodB.CHO
		lipid:float = ma*self.Lipid + mb*foodB.Lipid
		protein = ma*self.Protein + mb*foodB.Protein
		ash:float = ma*self.Ash + mb* foodB.Ash
		salt:float = ma*self.Salt + mb* foodB.Salt

		sum = water + CHO + lipid + protein + ash + salt

		water=water/sum*100
		CHO=CHO/sum*100	
		lipid=lipid/sum*100
		protein=protein/sum*100 
		ash=ash/sum*100
		salt=salt/sum*100


		retFood = Food(water=water, CHO=CHO, lipid=lipid, protein=protein, ash=ash, salt=salt)
		retFood.weight= ma + mb
	
		#if the other food's temperature is negligibly different than
		#mixtures temperature is one of the food items' temperature
		if(math.isclose(Ta, Tb, rel_tol=1E-5)):
			retFood.temperature = Ta
		
		else:
			E1 , E2 = ma*cpa*Ta, mb*cpb*Tb
			cp_avg = (cpa + cpb)/2.0
			mtot = ma + mb
			Tmix=(E1 + E2)/(mtot*cp_avg)
		
			retFood.temperature = Tmix

		return retFood


	

	def __sub__(self, foodB:Food)->Food:	
		ma, mb = self.weight,  foodB.weight
		Ta, Tb = self.temperature, foodB.temperature 
		mdiff = ma - mb

		if mdiff < 0:
			raise ValueError("Weight can not be smaller than or equal to zero")

		if math.isclose(Ta, Tb, rel_tol=1E-5):
			raise ValueError("In subtraction Foods cannot have different temperatures.")

		fA, fB=self.getIngredients(), foodB.getIngredients()

		#check if there are common ingredients
		NamesA, NamesB=set(), set()

		for k in fA.keys():
			NamesA.add(k)

		for k in fB.keys():
			NamesB.add(k)

		if(len(NamesA.intersection(NamesB))==0):
			raise Exception("No common ingredient found")


		newFood={}
		
		for k, v in fA.items():
			if(fB.get(k)!=None):
				diff_val=ma*v-mb*fB[k]
				assert diff_val>=0, "Weight of " + k + " can not be smaller than zero"
				
				if(math.math.isclose(diff_val, 0.0, abs_tol=1E-5)):
					diff_val=0
			
			newFood[k]=diff_val



		Total=sum(newFood.values(), 0)



		for k,v in newFood.items():
			newFood[k]=float(v)/Total*100
		

		retFood=Food(**newFood)
		retFood.weight = ma-mb


		return retFood




	def __mul__(self, elem:float)->Food:
		if(not isinstance(elem, numbers.Number)):
			raise Exception("Foods can only be multiplied by numbers")
	 

		newFood=self.getIngredients()

		retFood=Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood




	def __rmul__(self, elem:float)->Food:
		if(not isinstance(elem, numbers.Number)):
			raise Exception("Foods can only be multiplied by numbers")
	 

		newFood=self.getIngredients()

		retFood=Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood

	

	def __str__(self):
		retStr=""

		retStr = retStr + "Weight (unit weight)=" + str(round(self.weight, 2)) +"\n"

		retStr = retStr + "Temperature (C)=" + str(round(self.temperature, 2)) +"\n"

		if(self.m_Water>0): 
			retStr = retStr + "Water (%)=" + str(round(self.m_Water, 2)) +"\n" 

		if(self.m_Protein>0): 
			retStr = retStr + "Protein (%)=" + str(round(self.m_Protein, 2)) +"\n" 
		
		if(self.m_CHO>0): 
			retStr = retStr + "CHO (%)=" + str(round(self.m_CHO, 2)) +"\n" 
		

		if(self.m_Lipid>0): 
			retStr = retStr + "Lipid (%)=" + str(round(self.m_Lipid, 2)) +"\n"
	

		if(self.m_Ash>0): 
			retStr = retStr + "Ash (%)=" + str(round(self.m_Ash, 2)) +"\n" 
		

		if(self.m_Salt>0): 
			retStr = retStr + "Salt (%)=" + str(round(self.m_Salt)) +"\n" 
		

		retStr = retStr + "Aw=" + str(round(self.aw(), 3)) + "\n"
		
		retStr = retStr + "pH=" + str(round(self.m_ph, 3)) + "\n"

		return retStr



	
	def __eq__(self, foodB:Food)->bool:

		if(not isinstance(foodB, Food)):
			return False

		fA, fB=self.getIngredients(), foodB.getIngredients()

		#fA and fB have the same keys but different values: v is the value for fA and fB[k] returns corresponding key value in foodB
		for k,v in fA.items():
			if(fB.get(k)==None):
				return False

			if(math.math.isclose(v, fB[k], rel_tol=1E-5)):
				return False
			
		return True



#only allow as a module
if __name__=='main':
	pass
