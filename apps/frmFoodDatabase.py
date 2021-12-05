import wx
import sqlite3 as sql

import scisuit.gui as gui
import scisuit.proceng as eng


class pnlSearch ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.m_FirstLDown = True
		self.m_Connection = sql.connect(gui.exepath() + "datafiles/USDANALSR28.db")

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
			SearchTxt = "%" + Txt + "%"
			rows = cursor.execute(QueryString , (SearchTxt,)).fetchall() 
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




class pnlProperties ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
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

		# Connect Events
		self.m_txtT.Bind( wx.EVT_TEXT, self.txtT_OnText )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def txtT_OnText( self, event ):
		event.Skip()





class frmFoodDatabase ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, 
            id = wx.ID_ANY, 
            title = wx.EmptyString, 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pnlSearch = pnlSearch( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook.AddPage( self.m_pnlSearch, u"Search", False )
		self.m_pnlProps =pnlProperties( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook.AddPage( self.m_pnlProps, u"Thermo-Physical Props", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	


if __name__=="__main__":
	frm=frmFoodDatabase(None) 
	frm.Show()