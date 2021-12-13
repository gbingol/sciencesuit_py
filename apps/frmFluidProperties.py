import wx

import scisuit.gui as gui

import scisuit.proceng.fluids as fluid



class pnlRefrigerantSaturated ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.m_txtBGChanged  = None
		self.m_FluidType = None
		self.m_SelectedProperty = None
		self.m_Parent = parent.GetParent()
		
		
		
		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticFluidType.Wrap( -1 )

		sizerFluidType.Add( self.m_staticFluidType, 0, wx.ALL, 5 )

		m_choiceFluidTypeChoices = []
		self.m_choiceFluidType = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceFluidTypeChoices, 0 )
		self.m_choiceFluidType.SetSelection( 0 )
		sizerFluidType.Add( self.m_choiceFluidType, 1, wx.ALL, 5 )


		mainSizer.Add( sizerFluidType, 1, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

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
		
		self.m_CtrlList = [[self.m_txtT, "T"], [self.m_txtP, "P"], 
            [self.m_txtVf, "vf"], [self.m_txtVg, "vg"],
            [self.m_txtHf, "hf"], [self.m_txtHg, "hg"],
            [self.m_txtSf, "sf"], [self.m_txtSg, "sg"]]


		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.FluidType_OnChoice )
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


	def OnInitDialog( self, event ):
		refrigerant = fluid.Refrigerant()
		self.m_FluidList = refrigerant.GetFluidNames()
	
		for entry in self.m_FluidList:
			Name = str(entry[0])
			Alternative = str(entry[1])
			if(len(Alternative)>7):
				Alternative = Alternative[0:int(len(Alternative)/2)] + "..." + Alternative[-int(len(Alternative)/4):]
			
			self.m_choiceFluidType.Append(Name +", "+ Alternative)
		event.Skip()
		
		
	def FluidType_OnChoice( self, event ):
		sel = event.GetSelection()
		self.m_FluidType = self.m_FluidList[sel][0] #name
		event.Skip()

	
	def radioT_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtT)
		self.m_SelectedProperty = "T"
		event.Skip()

	def radioP_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtP)
		self.m_SelectedProperty = "P"
		event.Skip()

	def radioVf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtVf)
		self.m_SelectedProperty = "vf"
		event.Skip()

	def radioVg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtVg)
		self.m_SelectedProperty = "vg"
		event.Skip()

	def radioHf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtHf)
		self.m_SelectedProperty = "hf"
		event.Skip()

	def radioHg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtHg)
		self.m_SelectedProperty = "hg"
		event.Skip()

	def radioSf_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtSf)
		self.m_SelectedProperty = "sf"
		event.Skip()

	def radioSg_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtSg)
		self.m_SelectedProperty = "sg"
		event.Skip()


	def btnCompute_OnButtonClick( self, event ):
		if self.m_FluidType == None:
			wx.MessageBox("Fluid type must be selected")
			return
		
		fl = fluid.SaturatedRefrigerant(self.m_FluidType ) 
		result = dict()
		try:
			result = fl.search(self.m_SelectedProperty, float(self.m_txtBGChanged.GetValue()))
		except Exception as e:
			wx.MessageBox(str(e))
			return
            
		for lst in self.m_CtrlList:
			if lst[0] == self.m_txtBGChanged:
				continue
			Value = result.get(lst[1])
			Digits = self.m_Parent.GetDigits() 
			if(Digits != None):
				lst[0].SetValue(str(round(Value, Digits)))
			else:
				lst[0].SetValue(str(Value)) 

		event.Skip()
	
	
	def Export(self):
		ws = gui.Worksheet()
		ws[0,0] = self.m_SelectedProperty
		ws[0,1] = self.m_txtBGChanged.GetValue()
		
		row = 2
		for lst in self.m_CtrlList: 
			if lst[0] == self.m_txtBGChanged:
				continue
			Name = lst[1]
			Value = lst[0].GetValue()
			ws[row, 0] = str(Name)
			ws[row,1] = str(Value)
			
			row += 1







class frmPropertiesofFluids ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Properties of Fluids" )
		
		self.m_Digits = None

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pnlSaturated = pnlRefrigerantSaturated( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Saturated" )
		self.m_pnlSaturated.InitDialog()
		self.m_notebook.AddPage( self.m_pnlSaturated, u"Saturated", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menuExport = wx.Menu()
		self.m_menuItemWorksheet = wx.MenuItem( self.m_menuExport, wx.ID_ANY, u"Worksheet", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuExport.Append( self.m_menuItemWorksheet )

		self.m_menubar.Append( self.m_menuExport, u"Export" )

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

		self.m_menubar.Append( self.m_menuDigits, u"Digits" )
		self.SetMenuBar( self.m_menubar )


		self.Centre( wx.BOTH )

		self.Bind( wx.EVT_MENU, self.menuItemWorksheet_OnMenuSelection, id = self.m_menuItemWorksheet.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItem2_OnMenuSelection, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItem3_OnMenuSelection, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItem4_OnMenuSelection, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.menuItem_AsIs_OnMenuSelection, id = self.m_menuItem_AsIs.GetId() )

	def __del__( self ):
		pass

	
	def menuItemWorksheet_OnMenuSelection( self, event ):
		curPage = self.m_notebook.GetCurrentPage()
		curPage.Export()
		
		event.Skip()
	
	def menuItem2_OnMenuSelection( self, event ):
		self.m_Digits = 2
		event.Skip()

	def menuItem3_OnMenuSelection( self, event ):
		self.m_Digits = 3
		event.Skip()

	def menuItem4_OnMenuSelection( self, event ):
		self.m_Digits = 4
		event.Skip()

	def menuItem_AsIs_OnMenuSelection( self, event ):
		self.m_Digits = None
		event.Skip()

	def GetDigits(self):
            return self.m_Digits


if __name__ == "__main__":
	frm = frmPropertiesofFluids(None) 
	frm.Show()