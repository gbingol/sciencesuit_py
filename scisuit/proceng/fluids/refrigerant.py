import sqlite3 as sql

from scisuit.proceng.fluids.fluid import Fluid

import scisuit.gui as gui




class Refrigerant(Fluid):
	"""
	Base class thermodynamic properties of refrigerants
	"""
	s_DataBasePath = gui.exepath() + "/datafiles/refrigerants.db"
	
	def __init__(self) -> None: 
		super().__init__()
		self.m_Connection = sql.connect(self.s_DataBasePath) 
	

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

        
		if(len(rows) == 0):
			QueryString = "SELECT * FROM MAINTABLE where ALTERNATIVE=?"
			rows = cursor.execute(QueryString , (FluidName,)).fetchall()

			#all options exhausted, raise an error
			if(len(rows)==0):
				raise ValueError(FluidName + " did not match any")
            
			self.m_DBTable = rows[0][2]
        
		#len(rows) ==1
		else:
			self.m_DBTable = rows[0][2]


	
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
		super().Init(FluidName)
		
		


	def __del__( self ):
		self.m_Connection.close()


	def search(self, PropertyName:str, QueryValue:float, Sort = True): 
		return self.searchOrderedTable(self.m_DBTable, PropertyName, QueryValue, Sort) 