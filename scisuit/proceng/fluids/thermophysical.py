import sqlite3 as sql

from scisuit.proceng.fluids.fluid import Fluid

import scisuit.gui as gui



class ThermoPhysical(Fluid):
	"""
	Thermo-physical properties (T, rho, cp, viscosity, k, Pr) of fluids
	"""

	def __init__(self, FluidName:str) -> None:
		"""
		FluidName: Name of the fluid
		"""
		super().__init__() 

		self.m_Connection = sql.connect(self.s_DataBasePath) 
		
		self.m_FluidName = FluidName
		cursor = self.m_Connection.cursor()

		"""
		Check if the parameter FluidName is valid
		Note that the columns in the database is configured as
		COLLATE NOCASE, therefore search is not case-sensitive
		"""
		QueryString = "SELECT * FROM MAINTABLE where NAME=?"
		rows = cursor.execute(QueryString , (FluidName,)).fetchall()

		#more than 1 name matches
		if(len(rows)>1):
			raise ValueError("More than 1 fluid matched the name:" + FluidName)

		self.m_DBTable = rows[0][2]


	def __del__( self ):
		self.m_Connection.close()

	
	def GetFluidNames(self):
		QueryString = "SELECT name FROM MAINTABLE"
		rowList = self.m_Connection.cursor().execute(QueryString , []).fetchall()
		
		return rowList


	def search(self, PropertyName:str, QueryValue:float, Sort:bool = True): 
		return self.searchOrderedTable(self.m_DBTable, PropertyName, QueryValue, Sort) 
            
	   

if __name__ == "__main__":
	r=ThermoPhysical("water")
	result = r.search("T", 22)
	
	print(result)
