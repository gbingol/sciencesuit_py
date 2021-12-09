import math
from sqlite3.dbapi2 import Cursor
#from .fluid import Fluid

import sqlite3 as sql

class Refrigerant:
    """
    Base class thermodynamic properties of refrigerants
    """

    def __init__(self) -> None:
        super().__init__()
    

    def GetFieldNames(self, cursor:Cursor, TableName:str):
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
        
    

    def search(self, PropertyName:str, QueryValue:float):
        """
        --Table must be in the form of, for example
        	 P	T	s	vf
        	50	20	2	0.2
        	70	25	3	0.8
        
        if for example searching for properties at T=22 then the command is:
        search("T", 22)
        
        Returns a dict with keys P, T, s, vf and with values corresponding to T=22 (using interpolation)`
        """
        cursor = self.m_Connection.cursor()
        AllFieldNames = self.GetFieldNames(cursor, self.m_DBTable)

        if((PropertyName in AllFieldNames) == False):
            raise ValueError("Valid property names: " + str(AllFieldNames))
        
        #Check if the numbers are increasing or decreasing for the given property
        strQuery="SELECT "+ PropertyName +" FROM " + self.m_DBTable
        rows = cursor.execute(strQuery , []).fetchall()
	    
        """
        We select a value from the mid-point of the properties and subtract the value at the very beginning
	    if Diff>0, then the numbers are ascending otherwise descending order
        """
        Diff = rows[math.floor(len(rows)/2)][0] - rows[0][0]
        Ascending = True
        if(Diff<0):
            Ascending = False
        
        SearchedFieldNames = AllFieldNames
        AllFieldNames.remove(PropertyName)
        SearchedFieldNames = ",".join(AllFieldNames)
        PlaceHolderList = [PropertyName, QueryValue]
        
        QueryLarger="SELECT " + SearchedFieldNames + " FROM " + self.m_DBTable + " WHERE " + "? >= ?" 
        RowsLarger = cursor.execute(QueryLarger , PlaceHolderList).fetchall()

        QueryLarger="SELECT " + SearchedFieldNames + " FROM " + self.m_DBTable + " WHERE " + "? <= ?" 
        RowsSmaller = cursor.execute(QueryLarger , PlaceHolderList).fetchall()


if __name__ == "__main__":
    r=SaturatedRefrigerant("water")
    r.search("T", 22.0)
