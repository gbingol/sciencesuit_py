import sqlite3 as sql

from scisuit.proceng.fluids.fluid import Fluid

import scisuit.gui as gui




class Refrigerant(Fluid):
	"""
	Base class for thermodynamic properties of refrigerants
	"""
	s_DataBasePath = gui.exepath() + "/datafiles/refrigerants.db"
	
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
		
		"""
		Assumption is made that at a given pressure the property values
		are monotonically increasing (which is the case for T, V, H, S)
		"""
 
		strQuery="SELECT "+ Name +" FROM "+ self.m_DBTable + " WHERE P=? AND T<=? ORDER BY T DESC LIMIT 1"
		row = cursor.execute(strQuery , [P,Value]).fetchall()
		LowerRange =row[0][0]

		strQuery="SELECT " + Name +" FROM "+ self.m_DBTable + " WHERE P=? AND T>=? LIMIT 1"
		row = cursor.execute(strQuery , [P, Value]).fetchall()
		UpperRange = row[0][0]

		return LowerRange, UpperRange



	def searchPT(self, P:float, T:float):
		"""
		search for the values at a given pressure (kPa) and temperature (celcius)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		def FindProperties(Pressure: float, Temperature:float):
			TL, TH = self._BracketProperty(Pressure, "T", Temperature)

			#Find properties at Pressure and lower range of temperature 
			strQuery="SELECT V, H, S FROM "+ self.m_DBTable + " WHERE P=? AND T=?"
			
			row = cursor.execute(strQuery , [Pressure, TL]).fetchall()
			Vlow, Hlow, Slow =row[0][0], row[0][1], row[0][2]

			#Find properties at lPressure and Upper range of temperature 
			row = cursor.execute(strQuery , [Pressure, TH]).fetchall()
			Vup, Hup, Sup =row[0][0], row[0][1], row[0][2]

			V = self.Interpolation(TL, Vlow, TH, Vup, Temperature)
			H = self.Interpolation(TL, Hlow, TH, Hup, Temperature)
			S = self.Interpolation(TL, Slow, TH, Sup, Temperature)

			return V, H, S
		
		Vlow, Hlow, Slow = FindProperties(PL, T)
		Vup, Hup, Sup = FindProperties(PH, T)

		V = self.Interpolation(PL, Vlow, PH, Vup, P)
		H = self.Interpolation(PL, Hlow, PH, Hup, P)
		S = self.Interpolation(PL, Slow, PH, Sup, P)

		return V, H, S


if __name__ == "__main__":
	fl = SuperHeatedRefrigerant("water")
	V, H, S = fl.searchPT(P=500, T=225)
	print(V)
	print(H)
	print(S)
