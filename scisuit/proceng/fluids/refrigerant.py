import math
from sqlite3.dbapi2 import Cursor
#from .fluid import Fluid

import sqlite3 as sql


def Interpolation(x1, y1, x2, y2, val):
	if(x1 == x2): 
		return y1 
	
	m,n=0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * val + n



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

        #Index of the property in the columns of the table
        ParamIndex = -1
        try:
            ParamIndex = AllFieldNames.index(PropertyName)
        except:
            raise ValueError("Valid property names: " + str(AllFieldNames))
        
        strQuery="SELECT * FROM " + self.m_DBTable + " ORDER BY "+ PropertyName
        rows = cursor.execute(strQuery , []).fetchall()
        
        RowIndex = -1

        for i in range(len(rows)):
            Value = rows[i][ParamIndex]
            if(Value>=QueryValue):
                RowIndex = i
                break
        
        retDict = dict()

        if(RowIndex == 0):
            TupleIndex = -1
            for propName in AllFieldNames:
                TupleIndex += 1
                if(propName == PropertyName):
                    continue

                Value = rows[0][TupleIndex]
                retDict[propName] = Value

            return retDict
            
        
        if(RowIndex == -1):
            strQuery="SELECT min( {} ), max( {} ) FROM " + self.m_DBTable
            rows = cursor.execute(strQuery.format(PropertyName, PropertyName)).fetchone()      
            raise ValueError(PropertyName + " range: [" + str(rows[0]) + " , " + str(rows[1]) + "]")
        

        PropValHigh = rows[RowIndex][ParamIndex]
        PropValLow = rows[RowIndex - 1][ParamIndex]
        TupleIndex = -1
        for propName in AllFieldNames:
            TupleIndex += 1
            if(propName == PropertyName):
                continue

            ValueLow = rows[RowIndex - 1][TupleIndex]
            ValueHigh = rows[RowIndex][TupleIndex]
            Value = Interpolation(PropValLow, ValueLow, PropValHigh, ValueHigh, QueryValue)
            retDict[propName] = Value
        
        return retDict
            


       


if __name__ == "__main__":
    r=SaturatedRefrigerant("water")
    result = r.search("sg", 20.0)

    print(result)
