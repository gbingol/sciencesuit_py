import wx
import sqlite3 as sql

import scisuit.gui as gui
import scisuit.proceng as eng


class pnlSearch ( wx.Panel ):

	def __init__( self, 
		parent, 
		id = wx.ID_ANY, 
		pos = wx.DefaultPosition, 
		size = wx.Size( 500,300 ), 
		style = wx.TAB_TRAVERSAL, 
		name = wx.EmptyString ):


		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.m_FirstLDown = True
		self.m_Connection = sql.connect(gui.exepath() + "datafiles/USDANALSR28.db")
		self.m_Food = None

		sizerSearch = wx.BoxSizer( wx.VERTICAL )

		m_listSearchChoices = []
		self.m_listSearch = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listSearchChoices, 0 )
		sizerSearch.Add( self.m_listSearch, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_txtSearch = wx.TextCtrl( self, wx.ID_ANY, u"Start Typing to Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtSearch.SetBackgroundColour( wx.Colour( 192, 192, 192 ) )

		sizerSearch.Add( self.m_txtSearch, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizerAndFit( sizerSearch )
		self.Layout()

		# Connect Events
		self.m_listSearch.Bind( wx.EVT_LISTBOX, self.listSearch_OnListBox )
		self.m_txtSearch.Bind( wx.EVT_LEFT_DOWN, self.txtSearch_OnLeftDown )
		self.m_txtSearch.Bind( wx.EVT_TEXT, self.txtSearch_OnText )
		

	
	def listSearch_OnListBox( self, event ):
		SelText = self.m_listSearch.GetStringSelection()
		QueryString="SELECT * FROM Composition where FoodName= ?"

		cursor = self.m_Connection.cursor()

		PlaceHolderTxt = SelText
		rows = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall() [0]
		
		water = float(rows[2])
		protein = float(rows[3])
		lipid = float(rows[4])
		CHO = float(rows[5])
		ash = float(rows[6])
		
		try:
			self.m_Food = eng.Food(water=water, protein = protein, lipid=lipid, CHO= CHO, ash=ash)
		except Exception as e:
			wx.MessageBox(e)
		
		event.Skip()



	def txtSearch_OnLeftDown( self, event ):
		if(self.m_FirstLDown):
			self.m_txtSearch.SetValue("")
			self.m_FirstLDown = False

		event.Skip()



	def txtSearch_OnText( self, event ):
		Txt=self.m_txtSearch.GetValue()
		Txt=Txt.strip()

		if(len(Txt)<2):
			return
		
		cursor = self.m_Connection.cursor()

		#clear the list
		self.m_listSearch.Clear()
		
		#split the phrase based on empty character
		words=Txt.split()

		rows = None
		QueryString = "SELECT * FROM Composition where FoodName like ?"
		if(len(words) == 1):
			PlaceHolderTxt = "%" + Txt + "%"
			rows = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall() 
		else:
			for i in range(1, len(words)):
				QueryString += " INTERSECT SELECT * FROM Composition where FoodName like ?"  
			
			PlaceHolderLst=[]
			for word in  words:
				w="%"+word+"%"
				PlaceHolderLst.append(w)
			
			rows = cursor.execute(QueryString , PlaceHolderLst).fetchall() 
			
		

		for entry in rows:
			self.m_listSearch.Append(str(entry[1])) 


		event.Skip()

	
	def GetFood(self):
		return self.m_Food




class pnlProperties ( wx.Panel ):

	def __init__( self, parent, 
		id = wx.ID_ANY, 
		pos = wx.DefaultPosition, 
		size = wx.Size( 500,300 ), 
		style = wx.TAB_TRAVERSAL, 
		name = wx.EmptyString ):

		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		sizerMain = wx.BoxSizer( wx.VERTICAL )

		sizerTemperature = wx.BoxSizer( wx.HORIZONTAL )

		self.m_statT = wx.StaticText( self, wx.ID_ANY, u"T (°C):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statT.Wrap( -1 )

		sizerTemperature.Add( self.m_statT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtT.SetToolTip( u"[0, 50]" )

		sizerTemperature.Add( self.m_txtT, 1, wx.ALL, 5 )


		sizerMain.Add( sizerTemperature, 0, wx.EXPAND, 5 )


		sizerMain.Add( ( 0, 10), 0, wx.EXPAND, 5 )

		sizerLeftRight = wx.BoxSizer( wx.HORIZONTAL )

		fgSizerIngredients = wx.FlexGridSizer( 0, 2, 10, 0 )
		fgSizerIngredients.AddGrowableCol( 1 )
		fgSizerIngredients.SetFlexibleDirection( wx.BOTH )
		fgSizerIngredients.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_statWater = wx.StaticText( self, wx.ID_ANY, u"Water", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statWater.Wrap( -1 )

		fgSizerIngredients.Add( self.m_statWater, 0, wx.ALL, 5 )

		self.m_txtWater = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtWater, 1, wx.ALL, 5 )

		self.m_statCHO = wx.StaticText( self, wx.ID_ANY, u"CHO", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statCHO.Wrap( -1 )

		fgSizerIngredients.Add( self.m_statCHO, 0, wx.ALL, 5 )

		self.m_txtCHO = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtCHO, 1, wx.ALL, 5 )

		self.m_statProtein = wx.StaticText( self, wx.ID_ANY, u"Protein", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statProtein.Wrap( -1 )

		fgSizerIngredients.Add( self.m_statProtein, 0, wx.ALL, 5 )

		self.m_txtProtein = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtProtein, 1, wx.ALL, 5 )

		self.m_statLipid = wx.StaticText( self, wx.ID_ANY, u"Lipid", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statLipid.Wrap( -1 )

		fgSizerIngredients.Add( self.m_statLipid, 0, wx.ALL, 5 )

		self.m_txtLipid = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtLipid, 1, wx.ALL, 5 )

		self.m_statAsh = wx.StaticText( self, wx.ID_ANY, u"Ash", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statAsh.Wrap( -1 )

		fgSizerIngredients.Add( self.m_statAsh, 0, wx.ALL, 5 )

		self.m_txtAsh = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtAsh, 1, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizerIngredients, 1, wx.EXPAND, 5 )

		fgSizerThermPhys = wx.FlexGridSizer( 0, 3, 10, 0 )
		fgSizerThermPhys.AddGrowableCol( 1 )
		fgSizerThermPhys.SetFlexibleDirection( wx.BOTH )
		fgSizerThermPhys.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_statRho = wx.StaticText( self, wx.ID_ANY, u"\u03C1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statRho.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statRho, 0, wx.ALL, 5 )

		self.m_txtRho = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtRho, 1, wx.ALL, 5 )

		self.m_statRhoUnit = wx.StaticText( self, wx.ID_ANY, u"kg/m3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statRhoUnit.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statRhoUnit, 0, wx.ALL, 5 )

		self.m_statK = wx.StaticText( self, wx.ID_ANY, u"k", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statK.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statK, 0, wx.ALL, 5 )

		self.m_txtK = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtK, 0, wx.ALL, 5 )

		self.m_statKUnit = wx.StaticText( self, wx.ID_ANY, u"W/mK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statKUnit.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statKUnit, 0, wx.ALL, 5 )

		self.m_statCp = wx.StaticText( self, wx.ID_ANY, u"Cp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statCp.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statCp, 0, wx.ALL, 5 )

		self.m_txtCp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtCp, 0, wx.ALL, 5 )

		self.m_statCpUnit = wx.StaticText( self, wx.ID_ANY, u"kJ/kg°C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statCpUnit.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statCpUnit, 0, wx.ALL, 5 )

		self.m_statAlpha = wx.StaticText( self, wx.ID_ANY, u"\u03B1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_statAlpha.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_statAlpha, 0, wx.ALL, 5 )

		self.m_txtAlpha = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtAlpha, 0, wx.ALL, 5 )

		self.m_staticAlphaUnit = wx.StaticText( self, wx.ID_ANY, u"m2/s", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticAlphaUnit.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticAlphaUnit, 0, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizerThermPhys, 1, wx.EXPAND, 5 )


		sizerMain.Add( sizerLeftRight, 1, wx.EXPAND, 5 )


		self.SetSizer( sizerMain )
		self.Layout()

		self.m_txtT.Bind( wx.EVT_TEXT, self.txtT_OnText )

	
	def SetWater(self, water:float):
		self.m_txtWater.SetValue(str(water))

	def SetProtein(self, protein:float):
		self.m_txtProtein.SetValue(str(protein))

	def SetLipid(self, lipid:float):
		self.m_txtLipid.SetValue(str(lipid))
	
	def SetCHO(self, CHO:float):
		self.m_txtCHO.SetValue(str(CHO))

	def SetAsh(self, ash:float):
		self.m_txtAsh.SetValue(str(ash))
	
	def SetK(self, k:float):
		self.m_txtK.SetValue(str(k))
	
	def SetRho(self, rho:float):
		self.m_txtRho.SetValue(str(rho))
	
	def SetCp(self, cp:float):
		self.m_txtCp.SetValue(str(cp))

	def SetAlpha(self, alpha:float):
		self.m_txtAlpha.SetValue(str(alpha))

	def GetTemperatureTxt(self):
		return self.m_txtT

	
	def txtT_OnText( self, event ):
		event.Skip()





class frmFoodDatabase ( gui.Frame ):
	"""
	1) The compositional data was downloaded from USDA NAL website (given below) as an Excel file.
	https://www.ars.usda.gov/northeast-area/beltsville-md/
	beltsville-human-nutrition-research-center/nutrient-data-laboratory/docs/sr28-download-files/
	
	2) Some of the characters such as & and , was replaced with empty characters for food names.
	3) Acronyms such as W/ and WO/ was replaced with with and without, respectively.
	4) Compositional Data (water, CHO, protein, total lipids, ash) was read from the 
	Excel file into database/USDANALSR28.db SQLite file.
	"""

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, 
            id = wx.ID_ANY, 
            title = "Search Food Database File - SR 28 (Offline)", 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		icon = wx.Icon()
		image = wx.Image()
		image.LoadFile(gui.exepath()+"apps/images/fooddatabase.jpg")
		bmp=image.ConvertToBitmap()
		icon.CopyFromBitmap(bmp)
		self.SetIcon(icon)

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pnlSearch = pnlSearch( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
		self.m_pnlProps =pnlProperties( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
		self.m_notebook.AddPage( self.m_pnlSearch, u"Search", False )
		self.m_notebook.AddPage( self.m_pnlProps, u"Thermo-Physical Props", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		self.m_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged )
		self.m_pnlProps.GetTemperatureTxt().Bind( wx.EVT_TEXT, self.txtT_OnText )
	

	def OnNotebookPageChanged( self, event ):
		selPage = self.m_notebook.GetSelection()

		if(selPage == 1):
			food = self.m_pnlSearch.GetFood()
			self.m_pnlProps.SetWater(round(food.Water, 2))
			self.m_pnlProps.SetProtein(round(food.Protein, 2))
			self.m_pnlProps.SetLipid(round(food.Lipid, 2))
			self.m_pnlProps.SetCHO(round(food.CHO, 2))
			self.m_pnlProps.SetAsh(round(food.Ash, 2))
			
			self.m_pnlProps.SetRho(round(food.rho(), 2))
			self.m_pnlProps.SetCp(round(food.cp(), 3))
			self.m_pnlProps.SetK(round(food.k(), 3))

			alpha=food.k() / (food.rho()*food.cp())
			self.m_pnlProps.SetAlpha(round(alpha, 5))

		event.Skip()
	

	def txtT_OnText( self, event ):
		txt = self.m_pnlProps.GetTemperatureTxt().GetValue()

		if(txt == ""):
			self.m_pnlProps.GetTemperatureTxt().SetBackgroundColour(wx.Colour(255, 255, 255))
			self.m_pnlProps.GetTemperatureTxt().Refresh()
			return
		
		Temperature = float(txt)

		if(Temperature<2 or Temperature>50):
			self.m_pnlProps.GetTemperatureTxt().SetToolTip(u"Thermo-physical predictions are not reliable")
			self.m_pnlProps.GetTemperatureTxt().SetBackgroundColour(wx.Colour(255, 0, 0))
			self.m_pnlProps.GetTemperatureTxt().Refresh()
		else:
			self.m_pnlProps.GetTemperatureTxt().SetToolTip(u"[2, 50]")
			self.m_pnlProps.GetTemperatureTxt().SetBackgroundColour(wx.Colour(255, 255, 255))
			self.m_pnlProps.GetTemperatureTxt().Refresh()

		food = self.m_pnlSearch.GetFood()
		food.temperature = Temperature
		self.m_pnlProps.SetRho(round(food.rho(), 2))
		self.m_pnlProps.SetCp(round(food.cp(), 3))
		self.m_pnlProps.SetK(round(food.k(), 3))

		alpha=food.k() / (food.rho()*food.cp())
		self.m_pnlProps.SetAlpha(round(alpha, 5))

		event.Skip()


if __name__=="__main__":
	frm=frmFoodDatabase(None) 
	frm.Show()