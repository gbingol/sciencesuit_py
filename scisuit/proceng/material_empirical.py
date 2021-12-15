from .material import Material



def Interpolation(x1, y1, x2, y2, val):
	if(x1 == x2): 
		return y1 
	
	m,n=0, 0
	m = (y2 - y1) / (x2 - x1)
	n = y2 - m * x2

	return m * val + n


class EmpiricalMaterial(Material):
	"""
	Base class for all materials whose properties are already in a database
	"""
	def __init__(self) -> None: 
		super().__init__()

		#database connection object
		self.m_Connection = None

		#private member to hold all the data in a table
		self._rows = None


	def GetConnection(self):
		"""
		Connection to database where properties are
		"""
		return self.m_Connection


	def GetFieldNames(self, TableName: str):
		"""
		Given a TableName returns all fieldnames (properties) of the table
		"""
		QueryString = "SELECT name FROM PRAGMA_TABLE_INFO(?)"
		rowList = self.m_Connection.cursor().execute(QueryString , (TableName,)).fetchall()

		if(len(rowList) == 0):
			raise ValueError("Invalid table name:" + TableName)

		retList = []
		for tupleItem in rowList:
			retList.append(tupleItem[0])

		return retList
	

	def searchOrderedTable(self, TableName:str, PropertyName:str, QueryValue:float, Sort:bool = True):
		"""
			TableName: Database table name where uniquely named properties are <br>
			PropertyName: Name of the property corresponding to fieldname in the table <br>
			QueryValue: Value at which properties are sought after <br>
			Sort: Sort the table based on the property name in ascending order 
			(if multiple queries are performed on the same property, set Sort to False for efficiency )
			
			--Table must be in the form of, for example <br>
			P	T	s	vf <br>
			50	20	2	0.2 <br>
			70	25	3	0.8 <br>
			
			if we are after properties at T=22, then returns a dict with keys P, s corresponding to T=22`
		"""
		cursor = self.GetConnection().cursor() 
		AllFieldNames = self.GetFieldNames(TableName)

		#Index of the property in the columns of the table
		ParamIndex = -1
		try:
			"""
				note that we search in capitalized field names with capitalized PropertyName
				For example, user now can enter Pr, pr ... to find properties for Prandtl
				The table must contain only unique fields
			"""
			CapitalizedFiledNames = [s.capitalize() for s in AllFieldNames]
			ParamIndex = CapitalizedFiledNames.index(PropertyName.capitalize())
		except:
			raise ValueError("Valid property names: " + str(AllFieldNames))
		
		
		if(Sort or self._rows == None):
			strQuery = "SELECT * FROM " + TableName + " ORDER BY "+ PropertyName
			self._rows = cursor.execute(strQuery , []).fetchall()
		
		RowIndex = -1

		for i in range(len(self._rows)):
			Value = self._rows[i][ParamIndex]
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

				Value = self._rows[0][TupleIndex]
				retDict[propName] = Value

			return retDict
				
			
		if(RowIndex == -1):
			strQuery="SELECT min( {} ), max( {} ) FROM " + TableName 
			rows = cursor.execute(strQuery.format(PropertyName, PropertyName)).fetchone()      
			raise ValueError(PropertyName + " range: [" + str(rows[0]) + " , " + str(rows[1]) + "]")
			

		PropValHigh = self._rows[RowIndex][ParamIndex]
		PropValLow = self._rows[RowIndex - 1][ParamIndex] 
		TupleIndex = -1

		for propName in AllFieldNames: 
			TupleIndex += 1
			
			if(propName.capitalize() == PropertyName.capitalize()):
				continue 

			ValueLow = self._rows[RowIndex - 1][TupleIndex]
			ValueHigh = self._rows[RowIndex][TupleIndex]
			Value = Interpolation(PropValLow, ValueLow, PropValHigh, ValueHigh, QueryValue)
			retDict[propName] = Value
			
		return retDict