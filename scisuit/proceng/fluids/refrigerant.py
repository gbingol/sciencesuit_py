import sqlite3 as sql

from scisuit.proceng.fluids.fluid import Fluid

import scisuit.util as util



class Refrigerant(Fluid):
	"""
	Base class for thermodynamic properties of refrigerants
	"""
	s_DataBasePath = util.exepath() + "/datafiles/refrigerants.db"
	
	def __init__(self) -> None: 
		super().__init__()
		self.m_Connection = sql.connect(self.s_DataBasePath) 

		#-1:Compressed, 0:saturated, 1:superheated
		self.m_FluidState = None

		self.m_DBTable = None

	
	def __del__( self ):
		self.m_Connection.close()
	

	def Init(self, FluidName:str)->None:
		self.m_FluidName = FluidName
		cursor = self.m_Connection.cursor()

		"""
		Check if the parameter FluidName is valid
		Note that the columns in the database is configured as
		COLLATE NOCASE, therefore search is not case-sensitive
		"""
		QueryString = "SELECT * FROM MAINTABLE where NAME=?"
		rows = cursor.execute(QueryString , (FluidName,)).fetchall()

		#a name like "R" or "R1" will match more than 1
		if(len(rows)>1):
			raise ValueError("More than 1 fluid matched the name:" + FluidName)

		DBTableColPos = 2 #saturated, compressed
		if(self.m_FluidState == 1):
			DBTableColPos = 3
		
		if(len(rows) == 0):
			QueryString = "SELECT * FROM MAINTABLE where ALTERNATIVE=?"
			rows = cursor.execute(QueryString , (FluidName,)).fetchall()

			#all options exhausted, raise an error
			if(len(rows)==0):
				raise ValueError(FluidName + " did not match any")
            
			self.m_DBTable = rows[0][DBTableColPos]
        
		#len(rows) ==1
		else:
			self.m_DBTable = rows[0][DBTableColPos]



	def GetFluidNames(self):
		QueryString = "SELECT name, alternative FROM MAINTABLE"
		rowList = self.m_Connection.cursor().execute(QueryString , []).fetchall()
		
		return rowList
    



class SaturatedRefrigerant(Refrigerant):

	def __init__(self, FluidName:str) -> None:
		"""
		FluidName: Name of the fluid
		"""
		super().__init__() 

		self.m_FluidState = 0
		super().Init(FluidName)
		

	def search(self, PropertyName:str, QueryValue:float, Sort = True): 
		return self.searchOrderedTable(self.m_DBTable, PropertyName, QueryValue, Sort) 



class SuperHeatedRefrigerant(Refrigerant):

	def __init__(self, FluidName:str) -> None:
		"""
		FluidName: Name of the fluid
		"""
		super().__init__() 

		self.m_FluidState = 1 
		super().Init(FluidName)
	

	def _BracketPressure(self, P:float):
		cursor = self.m_Connection.cursor()

		QueryString = "SELECT min(P), max(P) FROM " + self.m_DBTable
		MinMax = cursor.execute(QueryString , []).fetchall()
		Pmin, Pmax = MinMax[0][0], MinMax[0][1]

		if(not (Pmin<P and P<Pmax)):
			raise ValueError("Pressure range: ["+ str(Pmin) + ", " + str(Pmax) + "]" )
		
		#Pressure is within limits, but where?
		strQuery="SELECT DISTINCT P FROM " + self.m_DBTable + " WHERE P<="+str(P) +" ORDER BY P DESC LIMIT 1"
		row = cursor.execute(strQuery , []).fetchall()
		PL =row[0][0]
		
		strQuery="SELECT DISTINCT P FROM " + self.m_DBTable + " WHERE P>="+ str(P) +" LIMIT 1"
		row = cursor.execute(strQuery , []).fetchall()
		PH =row[0][0]
		
		return PL, PH

	
	def _BracketProperty(self, P:float, Name:str , Value:float):
		"""
		given a pressure value, finds lower and upper range of property
		"""

		cursor = self.m_Connection.cursor()
		
		QueryString = "SELECT min("+ Name +"), max(" + Name +") FROM " + self.m_DBTable + " WHERE P=?"
		MinMax = cursor.execute(QueryString , [P]).fetchall()
		PropertyMin, PropertyMax = MinMax[0][0], MinMax[0][1]

		if(not (PropertyMin < Value and Value < PropertyMax)):
			raise ValueError("At P="+ str(P) + " kPa, " + Name + " has range: ["+ str(PropertyMin) + ", " + str(PropertyMax) + "]" )
		
		"""
		Assumption is made that at a given pressure the property values
		are monotonically increasing (which is the case for T, V, H, S)
		"""
 
		strQuery="SELECT "+ Name +" FROM "+ self.m_DBTable + " WHERE P=? AND " + Name + "<=? ORDER BY " + Name + " DESC LIMIT 1"
		row = cursor.execute(strQuery , [P,Value]).fetchall()
		LowerRange =row[0][0]

		strQuery="SELECT " + Name +" FROM "+ self.m_DBTable + " WHERE P=? AND "+ Name +">=? LIMIT 1"
		row = cursor.execute(strQuery , [P, Value]).fetchall()
		UpperRange = row[0][0]

		return LowerRange, UpperRange


	def _FindProperties(self, P: float, Name:str , Value:float):
		"""
		Given a pressure value and a property, i.e. temperature
		the function returns the properties at the given pressure and temperature
		
		Note that the pressure here is the lower or upper value of the bracketed pressure
		and NOT the exact pressure value requested by user
		
		Therefore for any search this function needs to be called twice: at lower and upper ranges of pressure
		"""
		cursor = self.m_Connection.cursor()

		PropLow, PropHigh = self._BracketProperty(P, Name, Value)

		AllFieldNames:list = self.GetFieldNames(self.m_DBTable)
		AllFieldNames.remove("P") #P is always known
		AllFieldNames.remove(Name.capitalize()) #property is known as well

		#As of this point AllFieldNames contains only the properties' names we are after
		JoinedFieldNames = ",".join(AllFieldNames)

		#Find properties at Pressure and lower range of the property 
		strQuery="SELECT " + JoinedFieldNames +" FROM "+ self.m_DBTable + " WHERE P=? AND "+ Name +"=?"
		
		"""
		Database table contains only fields of P, T, V, H, S
		Therefore once two properties are known, i.e., P and T,
		there remains 3 properties which are named arbitrarily as A, B, C
		"""
		
		row = cursor.execute(strQuery , [P, PropLow]).fetchall()
		Alow, Blow, Clow =row[0][0], row[0][1], row[0][2]

		#Find properties at lPressure and Upper range of the property 
		row = cursor.execute(strQuery , [P, PropHigh]).fetchall()
		Aup, Bup, Cup =row[0][0], row[0][1], row[0][2]

		A = self.Interpolation(PropLow, Alow, PropHigh, Aup, Value)
		B = self.Interpolation(PropLow, Blow, PropHigh, Bup, Value)
		C = self.Interpolation(PropLow, Clow, PropHigh, Cup, Value)

		return A, B, C


	def search_PT(self, P:float, T:float):
		"""
		search for the values at a given pressure (kPa) and temperature (celcius)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Vlow, Hlow, Slow = self._FindProperties(PL, "T", T)
		Vup, Hup, Sup = self._FindProperties(PH, "T", T)

		V = self.Interpolation(PL, Vlow, PH, Vup, P)
		H = self.Interpolation(PL, Hlow, PH, Hup, P)
		S = self.Interpolation(PL, Slow, PH, Sup, P)
		
		

		return {'V':V, 'H':H, 'S': S}
		
		
	def search_PV(self, P:float, V:float):
		"""
		search for the values at a given pressure (kPa) and specific volume (m3/kg)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Hlow, Slow = self._FindProperties(PL, "V", V)
		Tup, Hup, Sup = self._FindProperties(PH, "V", V)

		T = self.Interpolation(PL, Tlow, PH, Tup, P)
		H = self.Interpolation(PL, Hlow, PH, Hup, P)
		S = self.Interpolation(PL, Slow, PH, Sup, P)

		return {'T':T, 'H':H, 'S':S}
		
	
	def search_PH(self, P:float, H:float):
		"""
		search for the values at a given pressure (kPa) and enthalpy (kJ/kg)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Vlow, Slow = self._FindProperties(PL, "H", H)
		Tup, Vup, Sup = self._FindProperties(PH, "H", H)

		T = self.Interpolation(PL, Tlow, PH, Tup, P)
		V = self.Interpolation(PL, Vlow, PH,Vup, P)
		S = self.Interpolation(PL, Slow, PH, Sup, P)

		return {'T':T, 'V':V, 'S':S}
	
	
	def search_PS(self, P:float, S:float):
		"""
		search for the values at a given pressure (kPa) and entropy (kJ/kgK)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Vlow, Hlow = self._FindProperties(PL, "S",S)
		Tup, Vup, Hup = self._FindProperties(PH, "S", S)

		T = self.Interpolation(PL, Tlow, PH, Tup, P)
		V = self.Interpolation(PL, Vlow, PH,Vup, P)
		H = self.Interpolation(PL, Hlow, PH, Hup, P)

		return {'T':T, 'V':V, 'H':H} 
		
	
	def search(self, P:float, name:str, value:float):
		CapName = name.upper()
		if(CapName == "T"):
			return self.search_PT(P, value)
		
		elif (CapName =="V"):
			return self.search_PV(P, value)
		
		elif(CapName == "H"):
			return self.search_PH(P, value)
		
		elif(CapName == "S"):
			return self.search_PS(P, value)
		
		else:
			raise ValueError("name must be T, V, H or S")
