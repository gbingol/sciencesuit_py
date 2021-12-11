import wx

import scisuit.gui as gui

class pnlRefrigerantSaturated ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.m_txtBGChanged = None
	

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizerLeft = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerLeft.AddGrowableCol( 1 )
		fgSizerLeft.SetFlexibleDirection( wx.BOTH )
		fgSizerLeft.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_radioT = wx.RadioButton( self, wx.ID_ANY, u"T (°C)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioP = wx.RadioButton( self, wx.ID_ANY, u"P (kPa)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioP, 0, wx.ALL, 5 )

		self.m_txtP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVf = wx.RadioButton( self, wx.ID_ANY, u"vf (m\u00B3/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioVf, 0, wx.ALL, 5 )

		self.m_txtVf = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtVf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVg = wx.RadioButton( self, wx.ID_ANY, u"vg (m\u00B3/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioVg, 0, wx.ALL, 5 )

		self.m_txtVg = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtVg, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioHf = wx.RadioButton( self, wx.ID_ANY, u"hf (kJ/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioHf, 0, wx.ALL, 5 )

		self.m_txtHf = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtHf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioHg = wx.RadioButton( self, wx.ID_ANY, u"hg (kJ/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioHg, 0, wx.ALL, 5 )

		self.m_txtHg = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtHg, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioSf = wx.RadioButton( self, wx.ID_ANY, u"sf (kJ/kg\u00B7K)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioSf, 0, wx.ALL, 5 )

		self.m_txtSf = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtSf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioSg = wx.RadioButton( self, wx.ID_ANY, u"sg (kJ/kg\u00B7K)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioSg, 0, wx.ALL, 5 )

		self.m_txtSg = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtSg, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 0, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute", wx.DefaultPosition, wx.DefaultSize, 0 )
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.m_radioT.Bind( wx.EVT_RADIOBUTTON, self.radioT_OnRadioButton )
		self.m_radioP.Bind( wx.EVT_RADIOBUTTON, self.radioP_OnRadioButton )
		self.m_radioVf.Bind( wx.EVT_RADIOBUTTON, self.radioVf_OnRadioButton )
		self.m_radioVg.Bind( wx.EVT_RADIOBUTTON, self.radioVg_OnRadioButton )
		self.m_radioHf.Bind( wx.EVT_RADIOBUTTON, self.radioHf_OnRadioButton )
		self.m_radioHg.Bind( wx.EVT_RADIOBUTTON, self.radioHg_OnRadioButton )
		self.m_radioSf.Bind( wx.EVT_RADIOBUTTON, self.radioSf_OnRadioButton )
		self.m_radioSg.Bind( wx.EVT_RADIOBUTTON, self.radioSg_OnRadioButton )
		self.m_btnCompute.Bind( wx.EVT_BUTTON, self.btnCompute_OnButtonClick )

	def __del__( self ):
		pass

	
	def ChangeBGColor(self, txtCtrl):
		BGColor = wx.Colour(144,238,144)
		if(self.m_txtBGChanged != None):
			self.m_txtBGChanged.SetBackgroundColour(wx.Colour(255, 255, 255)) 
			self.m_txtBGChanged.Refresh()
		
		txtCtrl.SetBackgroundColour(BGColor)
		txtCtrl.Refresh()
		self.m_txtBGChanged = txtCtrl

	
	def radioT_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtT)
		event.Skip()

	def radioP_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtP)
		event.Skip()

	def radioVf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtVf)
		event.Skip()

	def radioVg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtVg)
		event.Skip()

	def radioHf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtHf)
		event.Skip()

	def radioHg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtHg)
		event.Skip()

	def radioSf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtSf)
		event.Skip()

	def radioSg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtSg)
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		event.Skip()







class frmPropertiesofFluids ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Properties of Fluids", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pnlSaturated = pnlRefrigerantSaturated( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Saturated" )
		self.m_notebook.AddPage( self.m_pnlSaturated, u"a page", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuExport = wx.Menu()
		self.m_menuItemWorksheet = wx.MenuItem( self.m_menuExport, wx.ID_ANY, u"Worksheet", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuExport.Append( self.m_menuItemWorksheet )

		self.m_menubar1.Append( self.m_menuExport, u"Export" )

		self.m_menuDigits = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"2 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem2 )

		self.m_menuItem3 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"3 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem3 )

		self.m_menuItem4 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"4 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem4 )

		self.m_menuItem_AsIs = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"As Is", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem_AsIs )
		self.m_menuItem_AsIs.Check( True )

		self.m_menubar1.Append( self.m_menuDigits, u"Digits" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.menuItemWorksheet_OnMenuSelection, id = self.m_menuItemWorksheet.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def menuItemWorksheet_OnMenuSelection( self, event ):
		event.Skip()



if __name__ == "__main__":
	frm = frmPropertiesofFluids(None) 
	frm.Show()