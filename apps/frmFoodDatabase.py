import wx

app=wx.App()

class pnlSearch ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

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

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def listSearch_OnListBox( self, event ):
		event.Skip()

	def txtSearch_OnLeftDown( self, event ):
		event.Skip()

	def txtSearch_OnText( self, event ):
		event.Skip()




class pnlProperties ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		sizerMain = wx.BoxSizer( wx.VERTICAL )

		sizerTemperature = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"T (°C):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		sizerTemperature.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizerTemperature.Add( self.m_txtT, 1, wx.ALL, 5 )


		sizerMain.Add( sizerTemperature, 0, wx.EXPAND, 5 )


		sizerMain.Add( ( 0, 10), 0, wx.EXPAND, 5 )

		sizerLeftRight = wx.BoxSizer( wx.HORIZONTAL )

		fgSizerIngredients = wx.FlexGridSizer( 0, 2, 10, 0 )
		fgSizerIngredients.AddGrowableCol( 1 )
		fgSizerIngredients.SetFlexibleDirection( wx.BOTH )
		fgSizerIngredients.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Water", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizerIngredients.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_txtWater = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtWater, 1, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"CHO", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizerIngredients.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_txtCHO = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtCHO, 1, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Protein", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizerIngredients.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_txtProtein = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtProtein, 1, wx.ALL, 5 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Lipid", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizerIngredients.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_txtLipid = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtLipid, 1, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Ash", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizerIngredients.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_txtAsh = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerIngredients.Add( self.m_txtAsh, 1, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizerIngredients, 1, wx.EXPAND, 5 )

		fgSizerThermPhys = wx.FlexGridSizer( 0, 3, 10, 0 )
		fgSizerThermPhys.AddGrowableCol( 1 )
		fgSizerThermPhys.SetFlexibleDirection( wx.BOTH )
		fgSizerThermPhys.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"\u03C1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.m_txtRho = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtRho, 1, wx.ALL, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"kg/m3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"k", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_txtK = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtK, 0, wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"W/mK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Cp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.m_txtCp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtCp, 0, wx.ALL, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"kJ/kg°C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"\u03B1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.m_txtAlpha = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerThermPhys.Add( self.m_txtAlpha, 0, wx.ALL, 5 )

		self.m_staticAlphaUnit = wx.StaticText( self, wx.ID_ANY, u"m2/s", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticAlphaUnit.Wrap( -1 )

		fgSizerThermPhys.Add( self.m_staticAlphaUnit, 0, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizerThermPhys, 1, wx.EXPAND, 5 )


		sizerMain.Add( sizerLeftRight, 1, wx.EXPAND, 5 )


		self.SetSizerAndFit( sizerMain )
		self.Layout()

	def __del__( self ):
		pass





class frmFoodDatabase ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, 
            id = wx.ID_ANY, 
            title = wx.EmptyString, 
            pos = wx.DefaultPosition, 
            size = wx.DefaultSize, 
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pnlSearch = pnlSearch( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook.AddPage( self.m_pnlSearch, u"a page", False )
		self.m_pnlProps =pnlProperties( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook.AddPage( self.m_pnlProps, u"a page", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass



frm=frmFoodDatabase(None)
frm.Show()

app.MainLoop()