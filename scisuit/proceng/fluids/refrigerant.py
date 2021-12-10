import sqlite3 as sql

from scisuit.proceng.fluids.fluid import Fluid
from scisuit.proceng.fluids.searchorderedtable import searchOrderedTable

import sqlite3 as sql






class Refrigerant(Fluid):
	"""
	Base class thermodynamic properties of refrigerants
	"""

	def __init__(self) -> None: 
		super().__init__()
    

	def GetFieldNames(self, cursor:sql.Cursor, TableName:str): 
		PlaceHolderTxt = TableName
		QueryString = "SELECT name FROM PRAGMA_TABLE_INFO(?)"
		rowList = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall()

		if(len(rowList) == 0):
			raise ValueError("Invalid table name:" + TableName)

		retList = []

		for tupleItem in rowList:
		   retList.append(tupleItem[0])

		return retList
    


class SaturatedRefrigerant(Refrigerant):
	"""
	FluidName: Name of the fluid
	PropertyName: Any property (P, T, vf, vg, sf, sg, hf, hg)
	Value: A numeric value of the property
	"""

	s_DataBasePath = "C:/datafiles/refrigerants.db"

	def __init__(self, FluidName:str) -> None:
		super().__init__() 
		self.m_FluidName = FluidName
		self.m_Connection = sql.connect(self.s_DataBasePath) 

		cursor = self.m_Connection.cursor()

		"""
            Check if the parameter FluidName is valid
            Note that the columns in the database is configured as
            COLLATE NOCASE, therefore search is not case-sensitive
		"""
		PlaceHolderTxt = FluidName
		QueryString = "SELECT * FROM MAINTABLE where NAME=?"
		rows = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall()

		#a name like "R" or "R1" will match more than 1
		if(len(rows)>1):
			raise ValueError("More than 1 fluid matched the name:" + FluidName)

        
		if(len(rows) == 0):
			QueryString = "SELECT * FROM MAINTABLE where ALTERNATIVE=?"
			rows = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall()

			#all options exhausted, raise an error
			if(len(rows)==0):
				raise ValueError(FluidName + " did not match any")
            
			self.m_DBTable = rows[0][2]
        
		#len(rows) ==1
		else:
			self.m_DBTable = rows[0][2]

	def GetConnection(self):
		return self.m_Connection

	def search(self, PropertyName:str, QueryValue:float): 
		return searchOrderedTable(self, self.m_DBTable, PropertyName, QueryValue) 
            
	   

if __name__ == "__main__":
	r=SaturatedRefrigerant("water")
	result = r.search("T", 22)
	
	print(result)
