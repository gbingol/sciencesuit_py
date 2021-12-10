import sqlite3 as sql
from  scisuit.proceng.fluids import Fluid

def Interpolation(x1, y1, x2, y2, val):
	if(x1 == x2): 
		return y1 
	
	m,n=0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * val + n


def searchOrderedTable(fluid:Fluid, TableName:str, PropertyName:str, QueryValue:float):
	"""
      fluid: a fluid type <br>
      TableName: Database table name <br>
      PropertyName: Name of the property, i.e. T for temperature <br>
      QueryValue: Value at which properties are sought after
      
      --Table must be in the form of, for example <br>
		P	T	s	vf <br>
      50	20	2	0.2 <br>
      70	25	3	0.8 <br>
      
      Returns a dict with keys P, T, s, vf and with values corresponding to T=22`
	"""
	cursor = fluid.GetConnection().cursor() 
	AllFieldNames = fluid.GetFieldNames(cursor, TableName)

	#Index of the property in the columns of the table
	ParamIndex = -1
	try:
		ParamIndex = AllFieldNames.index(PropertyName)
	except:
		raise ValueError("Valid property names: " + str(AllFieldNames))
        
	strQuery="SELECT * FROM " + TableName + " ORDER BY "+ PropertyName
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
		strQuery="SELECT min( {} ), max( {} ) FROM " + TableName 
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
        