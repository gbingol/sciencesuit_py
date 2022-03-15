import wx

import scisuit.gui as gui
import scisuit.proceng.fluids as fluid



class pnlRefrigerantSaturated ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent )

		self.m_txtBGChanged  = None
		self.m_FluidType = None
		self.m_SelectedProperty = None
		self.m_Parent = parent.GetParent()
			
		
		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
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

		self.m_radioT = wx.RadioButton( self, wx.ID_ANY, u"T (°C)")
		fgSizerLeft.Add( self.m_radioT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString)
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioP = wx.RadioButton( self, wx.ID_ANY, u"P (kPa)")
		fgSizerLeft.Add( self.m_radioP, 0, wx.ALL, 5 )

		self.m_txtP = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVf = wx.RadioButton( self, wx.ID_ANY, u"vf (m\u00B3/kg)")
		fgSizerLeft.Add( self.m_radioVf, 0, wx.ALL, 5 )

		self.m_txtVf = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtVf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVg = wx.RadioButton( self, wx.ID_ANY, u"vg (m\u00B3/kg)")
		fgSizerLeft.Add( self.m_radioVg, 0, wx.ALL, 5 )

		self.m_txtVg = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtVg, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioHf = wx.RadioButton( self, wx.ID_ANY, u"hf (kJ/kg)")
		fgSizerLeft.Add( self.m_radioHf, 0, wx.ALL, 5 )

		self.m_txtHf = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtHf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioHg = wx.RadioButton( self, wx.ID_ANY, u"hg (kJ/kg)")
		fgSizerLeft.Add( self.m_radioHg, 0, wx.ALL, 5 )

		self.m_txtHg = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtHg, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioSf = wx.RadioButton( self, wx.ID_ANY, u"sf (kJ/kg\u00B7K)")
		fgSizerLeft.Add( self.m_radioSf, 0, wx.ALL, 5 )

		self.m_txtSf = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtSf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioSg = wx.RadioButton( self, wx.ID_ANY, u"sg (kJ/kg\u00B7K)")
		fgSizerLeft.Add( self.m_radioSg, 0, wx.ALL, 5 )

		self.m_txtSg = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtSg, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 0, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute")
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
			
		if(self.m_SelectedProperty == None):
			wx.MessageBox("A property must be selected")
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





class pnlRefrigerantSuperheated ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent)
		
		self.m_FluidType = None
		self.m_Parent = parent.GetParent()
		self.m_NCheckedBoxes = 1 # pressure already checked

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
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

		self.m_chkT = wx.CheckBox( self, wx.ID_ANY, u"T (°C)" )
		fgSizerLeft.Add( self.m_chkT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkP = wx.CheckBox( self, wx.ID_ANY, u"P (kPa)")
		self.m_chkP.SetValue(True)
		self.m_chkP.Enable( False )

		fgSizerLeft.Add( self.m_chkP, 0, wx.ALL, 5 )

		self.m_txtP = wx.TextCtrl( self)
		self.m_txtP.SetBackgroundColour(wx.Colour(144,238,144))
		fgSizerLeft.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkV = wx.CheckBox( self, wx.ID_ANY, u"v (m\u00B3/kg)")
		fgSizerLeft.Add( self.m_chkV, 0, wx.ALL, 5 )

		self.m_txtV = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtV, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkH = wx.CheckBox( self, wx.ID_ANY, u"h (kJ/kg)")
		fgSizerLeft.Add( self.m_chkH, 0, wx.ALL, 5 )

		self.m_txtH = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtH, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkS = wx.CheckBox( self, wx.ID_ANY, u"s (kJ/kg\u00B7K)")
		fgSizerLeft.Add( self.m_chkS, 0, wx.ALL, 5 )

		self.m_txtS = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtS, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 0, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute" )
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_CtrlList = [
		[self.m_chkT, self.m_txtT,  "T"], 
		[self.m_chkV, self.m_txtV, "v"],
		[self.m_chkH, self.m_txtH, "h"],
		[self.m_chkS, self.m_txtS, "s"]]

		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.FluidType_OnChoice )
		self.m_chkT.Bind( wx.EVT_CHECKBOX, self.chkT_OnCheckBox )
		self.m_chkV.Bind( wx.EVT_CHECKBOX, self.chkV_OnCheckBox )
		self.m_chkH.Bind( wx.EVT_CHECKBOX, self.chkH_OnCheckBox )
		self.m_chkS.Bind( wx.EVT_CHECKBOX, self.chkS_OnCheckBox )
		self.m_btnCompute.Bind( wx.EVT_BUTTON, self.btnCompute_OnButtonClick )

	def __del__( self ):
		pass


	def EnableDisable(self, chkCtrl):
		BGColor = wx.Colour(144,238,144)
		if(chkCtrl.GetValue()):
			self.m_NCheckedBoxes += 1
		else:
			self.m_NCheckedBoxes -= 1
		
		
		for Ctrls in self.m_CtrlList:
			if(Ctrls[0] == chkCtrl):
				if(self.m_NCheckedBoxes == 2):
					Ctrls[1].SetBackgroundColour(BGColor) 
				else:
					Ctrls[1].SetBackgroundColour(wx.Colour(255, 255, 255)) 
				Ctrls[1].Refresh()
				continue
				
			if(self.m_NCheckedBoxes == 2):
				Ctrls[0].Enable(False)
				Ctrls[1].SetBackgroundColour(wx.Colour(255,204,204)) #light red
			else:
				Ctrls[0].Enable(True)
				Ctrls[1].SetBackgroundColour(wx.Colour(255,255,255)) 
			Ctrls[1].Refresh()

	
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

	def chkT_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkT)
		event.Skip()

	def chkV_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkV)
		event.Skip()

	def chkH_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkH)
		event.Skip()

	def chkS_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkS)
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		if self.m_FluidType == None:
			wx.MessageBox("Fluid type must be selected")
			return
		
		if self.m_NCheckedBoxes ==1:
			wx.MessageBox("Exactly two properties must be selected")
			return
		
		if(self.m_txtP.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for pressure")
			return
		
		SelectedProp:str = ""
		InputVal = ""
		for lst in self.m_CtrlList:
			if lst[0].GetValue() == True:
				SelectedProp = lst[2].upper()
				InputVal = lst[1].GetValue()
		
		if(InputVal == ""):
			wx.MessageBox("A value must be entered for " + SelectedProp)
			return
				
		fl = fluid.SuperHeatedRefrigerant(self.m_FluidType ) 
		
		result = dict()
		try:
			result = fl.search(float(self.m_txtP.GetValue()), SelectedProp, float(InputVal))
		except Exception as e:
			wx.MessageBox(str(e))
			return
		
		
		Digits = self.m_Parent.GetDigits()
		
		for Ctrl in  self.m_CtrlList:
			Value = result.get(Ctrl[2].capitalize())
			if(Value == None):
				continue
				
			if(Digits != None):
				Ctrl[1].SetValue(str(round(Value, Digits )))
			else:
				Ctrl[1].SetValue(str(Value))
		
		event.Skip()
	

	def Export(self):
		ws = gui.Worksheet()
		ws[0,0] = "P"
		ws[0,1] = self.m_txtP.GetValue()

		for lst in self.m_CtrlList: 
			if lst[0].GetValue():
				ws[1, 0] = lst[2]
				ws[1, 1] = lst[1].GetValue()

				break
		
		row = 3
		for lst in self.m_CtrlList: 
			if lst[0].GetValue():
				continue
			ws[row, 0] = str(lst[2]) #name
			ws[row,1] = str(lst[1].GetValue())
			
			row += 1





class pnlThermoPhysical ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent)
		
		self.m_txtBGChanged  = None
		self.m_FluidType = None
		self.m_SelectedProperty = None
		self.m_Parent = parent.GetParent()

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
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

		self.m_radioT = wx.RadioButton( self, wx.ID_ANY, u"T (°C)")
		fgSizerLeft.Add( self.m_radioT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioRho = wx.RadioButton( self, wx.ID_ANY, u"Density (kg/m\u00B3)")
		fgSizerLeft.Add( self.m_radioRho, 0, wx.ALL, 5 )

		self.m_txtRho = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtRho, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioCp = wx.RadioButton( self, wx.ID_ANY, u"Cp (kJ/kgK)")
		fgSizerLeft.Add( self.m_radioCp, 0, wx.ALL, 5 )

		self.m_txtCp = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtCp, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioK = wx.RadioButton( self, wx.ID_ANY, u"k (W/mK)")
		fgSizerLeft.Add( self.m_radioK, 0, wx.ALL, 5 )

		self.m_txtK = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtK, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioMu = wx.RadioButton( self, wx.ID_ANY, u"Viscosity (Pa s)")
		fgSizerLeft.Add( self.m_radioMu, 0, wx.ALL, 5 )

		self.m_txtMu = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtMu, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioPr = wx.RadioButton( self, wx.ID_ANY, u"Pr")
		fgSizerLeft.Add( self.m_radioPr, 0, wx.ALL, 5 )

		self.m_txtPr = wx.TextCtrl( self)
		fgSizerLeft.Add( self.m_txtPr, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 0, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute")
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_CtrlList = [[self.m_txtT, "T"], [self.m_txtRho, "rho"], 
            [self.m_txtCp, "cp"], [self.m_txtMu, "mu"],
            [self.m_txtK, "k"], [self.m_txtPr, "Pr"]]

		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.FluidType_OnChoice )
		self.m_radioT.Bind( wx.EVT_RADIOBUTTON, self.radioT_OnRadioButton )
		self.m_radioRho.Bind( wx.EVT_RADIOBUTTON, self.radioRho_OnRadioButton )
		self.m_radioCp.Bind( wx.EVT_RADIOBUTTON, self.radioCp_OnRadioButton )
		self.m_radioK.Bind( wx.EVT_RADIOBUTTON, self.radioK_OnRadioButton )
		self.m_radioMu.Bind( wx.EVT_RADIOBUTTON, self.radioMu_OnRadioButton )
		self.m_radioPr.Bind( wx.EVT_RADIOBUTTON, self.radioPr_OnRadioButton )
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
		fl = fluid.ThermoPhysical("")
		self.m_FluidList = fl.GetFluidNames()
	
		for entry in self.m_FluidList:
			self.m_choiceFluidType.Append(str(entry[0]))
		event.Skip()
	
	
	
	def FluidType_OnChoice( self, event ):
		sel = event.GetSelection()
		self.m_FluidType = self.m_FluidList[sel][0] 
		event.Skip()



	def radioT_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtT)
		self.m_SelectedProperty = "T"
		event.Skip()

	def radioRho_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtRho)
		self.m_SelectedProperty = "rho"
		event.Skip()

	def radioCp_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtCp)
		self.m_SelectedProperty = "cp"
		event.Skip()

	def radioK_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtK)
		self.m_SelectedProperty = "k"
		event.Skip()

	def radioMu_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtMu)
		self.m_SelectedProperty = "mu"
		event.Skip()

	def radioPr_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtPr)
		self.m_SelectedProperty = "pr"
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		if self.m_FluidType == None:
			wx.MessageBox("Fluid type must be selected")
			return
		
		if self.m_SelectedProperty == None:
			wx.MessageBox("A property must be selected")
			return
		
		
		if self.m_txtBGChanged.GetValue() == "":
			wx.MessageBox("A value must be entered for " + self.m_SelectedProperty)
			return
		
		fl = fluid.ThermoPhysical(self.m_FluidType ) 
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
		
		self.SetIcon(gui.makeicon("applications/engineering/images/fluid.bmp"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY)
		self.m_pnlSaturated = pnlRefrigerantSaturated( self.m_notebook )
		self.m_pnlSaturated.InitDialog()
		
		self.m_pnlSuperheated = pnlRefrigerantSuperheated( self.m_notebook)
		self.m_pnlSuperheated.InitDialog()
		
		self.m_pnlThermal = pnlThermoPhysical( self.m_notebook)
		self.m_pnlThermal.InitDialog()
		
		self.m_notebook.AddPage( self.m_pnlSaturated, u"Saturated", True )
		self.m_notebook.AddPage( self.m_pnlSuperheated, u"Superheated", False )
		self.m_notebook.AddPage( self.m_pnlThermal, u"Thermo-physical", False )

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