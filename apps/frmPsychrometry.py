
import time
import wx

import scisuit.proceng as eng
import scisuit.gui as gui

#app=wx.App()

class frmPsychrometry ( gui.Frame ):

	def __init__( self, parent ):
        
		gui.Frame.__init__ ( self, 
                parent, 
                id = wx.ID_ANY, 	
                title = u"Psychrometry", 
                pos = wx.DefaultPosition, 
                size = wx.Size( -1,-1 ), 
                style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )



		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 0, 242, 242 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerLeftRight = wx.BoxSizer( wx.HORIZONTAL )

		fgSizer_Left = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer_Left.SetFlexibleDirection( wx.BOTH )
		fgSizer_Left.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_chkP = wx.CheckBox( self, wx.ID_ANY, u"P", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_chkP.SetToolTip( u"Pressure" )

		fgSizer_Left.Add( self.m_chkP, 0, wx.ALL, 5 )

		self.m_txtP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtP.SetToolTip( u"Pressure" )

		fgSizer_Left.Add( self.m_txtP, 0, wx.ALL, 5 )

		self.m_lblP = wx.StaticText( self, wx.ID_ANY, u"kPa", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblP.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblP, 0, wx.ALL, 5 )

		self.m_stxtPw = wx.StaticText( self, wx.ID_ANY, u"Pw", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stxtPw.Wrap( -1 )

		fgSizer_Left.Add( self.m_stxtPw, 0, wx.ALL, 5 )

		self.m_txtPw = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer_Left.Add( self.m_txtPw, 0, wx.ALL, 5 )

		self.m_lblPw = wx.StaticText( self, wx.ID_ANY, u"kPa", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblPw.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblPw, 0, wx.ALL, 5 )

		self.m_stxtPws = wx.StaticText( self, wx.ID_ANY, u"Pws", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stxtPws.Wrap( -1 )

		fgSizer_Left.Add( self.m_stxtPws, 0, wx.ALL, 5 )

		self.m_txtPws = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer_Left.Add( self.m_txtPws, 0, wx.ALL, 5 )

		self.m_lblPws = wx.StaticText( self, wx.ID_ANY, u"kPa", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblPws.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblPws, 0, wx.ALL, 5 )

		self.m_chkTdb = wx.CheckBox( self, wx.ID_ANY, u"Tdb", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_chkTdb.SetToolTip( u"dry-bulb temperature" )

		fgSizer_Left.Add( self.m_chkTdb, 0, wx.ALL, 5 )

		self.m_txtTdb = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Left.Add( self.m_txtTdb, 0, wx.ALL, 5 )

		self.m_lblTdb = wx.StaticText( self, wx.ID_ANY, u"°C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblTdb.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblTdb, 0, wx.ALL, 5 )

		self.m_chkTwb = wx.CheckBox( self, wx.ID_ANY, u"Twb", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_chkTwb.SetToolTip( u"wet-bulb temperature" )

		fgSizer_Left.Add( self.m_chkTwb, 0, wx.ALL, 5 )

		self.m_txtTwb = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Left.Add( self.m_txtTwb, 0, wx.ALL, 5 )

		self.m_lblTwb = wx.StaticText( self, wx.ID_ANY, u"°C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblTwb.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblTwb, 0, wx.ALL, 5 )

		self.m_chkTdp = wx.CheckBox( self, wx.ID_ANY, u"Tdp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_chkTdp.SetToolTip( u"dew-point temperature" )

		fgSizer_Left.Add( self.m_chkTdp, 0, wx.ALL, 5 )

		self.m_txtTdp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Left.Add( self.m_txtTdp, 0, wx.ALL, 5 )

		self.m_lblTdp = wx.StaticText( self, wx.ID_ANY, u"°C", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblTdp.Wrap( -1 )

		fgSizer_Left.Add( self.m_lblTdp, 0, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizer_Left, 1, wx.EXPAND, 5 )

		fgSizer_Right = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer_Right.SetFlexibleDirection( wx.BOTH )
		fgSizer_Right.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_chkW = wx.CheckBox( self, wx.ID_ANY, u"W", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_chkW, 0, wx.ALL, 5 )

		self.m_txtW = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_txtW, 0, wx.ALL, 5 )

		self.m_lblW = wx.StaticText( self, wx.ID_ANY, u"kg/kgda", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblW.Wrap( -1 )

		fgSizer_Right.Add( self.m_lblW, 0, wx.ALL, 5 )

		self.m_stxtWs = wx.StaticText( self, wx.ID_ANY, u"Ws", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stxtWs.Wrap( -1 )

		fgSizer_Right.Add( self.m_stxtWs, 0, wx.ALL, 5 )

		self.m_txtWs = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer_Right.Add( self.m_txtWs, 0, wx.ALL, 5 )

		self.m_lblWs = wx.StaticText( self, wx.ID_ANY, u"kg/kgda", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblWs.Wrap( -1 )

		fgSizer_Right.Add( self.m_lblWs, 0, wx.ALL, 5 )

		self.m_chkH = wx.CheckBox( self, wx.ID_ANY, u"H", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_chkH, 0, wx.ALL, 5 )

		self.m_txtH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_txtH, 0, wx.ALL, 5 )

		self.m_lblH = wx.StaticText( self, wx.ID_ANY, u"kJ/kgda", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblH.Wrap( -1 )

		fgSizer_Right.Add( self.m_lblH, 0, wx.ALL, 5 )

		self.m_chkRH = wx.CheckBox( self, wx.ID_ANY, u"RH", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_chkRH, 0, wx.ALL, 5 )

		self.m_txtRH = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_txtRH, 0, wx.ALL, 5 )

		self.m_lblRH = wx.StaticText( self, wx.ID_ANY, u"%", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblRH.Wrap( -1 )

		fgSizer_Right.Add( self.m_lblRH, 0, wx.ALL, 5 )

		self.m_chkV = wx.CheckBox( self, wx.ID_ANY, u"v", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_chkV, 0, wx.ALL, 5 )

		self.m_txtV = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_Right.Add( self.m_txtV, 0, wx.ALL, 5 )

		self.m_lblV = wx.StaticText( self, wx.ID_ANY, u"m3/kg", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblV.Wrap( -1 )

		fgSizer_Right.Add( self.m_lblV, 0, wx.ALL, 5 )


		sizerLeftRight.Add( fgSizer_Right, 1, wx.EXPAND, 5 )


		mainSizer.Add( sizerLeftRight, 1, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 20), 0, wx.EXPAND, 5 )

		self.m_btnCalc = wx.Button( self, wx.ID_ANY, u"Calculate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnCalc.Enabled=False
		mainSizer.Add( self.m_btnCalc, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_menubar = wx.MenuBar( 0 )
		
		self.m_menuFile = wx.Menu()
		self.m_menuItemExport = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Export", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemExport )

		self.m_menubar.Append( self.m_menuFile, u"File" )
		
		self.m_menuDigits = wx.Menu()
		self.m_menuItem2Digits = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"2 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem2Digits )

		self.m_menuItem3Digits = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"3 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem3Digits )

		self.m_menuItem4Digits = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"4 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem4Digits )

		self.m_menubar.Append( self.m_menuDigits, u"Digits" )

		self.SetMenuBar( self.m_menubar )


		self.SetSizer( mainSizer )
		self.Layout()
		mainSizer.Fit( self )

		
		self.Centre( wx.BOTH )
		
		self.m_chkP.Bind( wx.EVT_CHECKBOX, self.chkP_OnCheckBox )
		self.m_chkTdb.Bind( wx.EVT_CHECKBOX, self.chkTdb_OnCheckBox )
		self.m_chkTwb.Bind( wx.EVT_CHECKBOX, self.chkTwb_OnCheckBox )
		self.m_chkTdp.Bind( wx.EVT_CHECKBOX, self.chkTdp_OnCheckBox )
		self.m_chkW.Bind( wx.EVT_CHECKBOX, self.chkW_OnCheckBox )
		self.m_chkH.Bind( wx.EVT_CHECKBOX, self.chkH_OnCheckBox )
		self.m_chkRH.Bind( wx.EVT_CHECKBOX, self.chkRH_OnCheckBox )
		self.m_chkV.Bind( wx.EVT_CHECKBOX, self.chkV_OnCheckBox )
		self.m_btnCalc.Bind( wx.EVT_BUTTON, self.btnCalc_OnButtonClick )
		
		self.Bind( wx.EVT_MENU, self.Export_OnMenuSelection, id = self.m_menuItemExport.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Digits, id = self.m_menuItem2Digits.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Digits, id = self.m_menuItem3Digits.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Digits, id = self.m_menuItem4Digits.GetId() )


		self.m_CheckBoxes=[self.m_chkP, 
				self.m_chkTdb, 
				self.m_chkTwb, 
				self.m_chkTdp, 
				self.m_chkW,
				self.m_chkH,
				self.m_chkRH,
				self.m_chkV  ]

		
		self.m_Controls=[
			[self.m_chkP, self.m_txtP, "Pressure", "P"],
			[self.m_chkTdb, self.m_txtTdb, "Dry-bulb temperature", "Tdb"],
			[self.m_chkTwb, self.m_txtTwb, "Wet-bulb temperature", "Twb"],
			[self.m_chkTdp, self.m_txtTdp, "Dew point temperature", "Tdp"],
			[self.m_chkW, self.m_txtW, "Absolute humidity", "W"],
			[self.m_chkH, self.m_txtH, "Enthalpy", "H"],
			[self.m_chkRH, self.m_txtRH, "Relative humidity", "RH"],
			[self.m_chkV, self.m_txtV, "Specific volume", "V"]
		]

	
	
	def EnableAllCheckBoxes(self):
		for chkBox in self.m_CheckBoxes:
			chkBox.Enable(True)
    


	def DisableUncheckedBoxes(self):
		for chkBox in self.m_CheckBoxes:
			if(chkBox.GetValue()==False):  #unchecked
				chkBox.Enabled=False
	


	def CheckToAllowStateChange(self):
		NumberofCheckedBoxes=0
		
		for chkBox in self.m_CheckBoxes:
			if(chkBox.GetValue()==True):
				NumberofCheckedBoxes += 1

		#If the number is 3, then disable unchecked boxes and allow calculation
		if(NumberofCheckedBoxes>=3):
			self.DisableUncheckedBoxes()
			self.m_btnCalc.Enabled=True
		else:
			self.EnableAllCheckBoxes()
			self.m_btnCalc.Enabled=False



	def __del__( self ):
		pass

    
    
	
	def chkP_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkTdb_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkTwb_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkTdp_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkW_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkH_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkRH_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()


	def chkV_OnCheckBox( self, event ):
		self.CheckToAllowStateChange()
		event.Skip()
		
	
	def Export_OnMenuSelection( self, event ):
		t=time.localtime()
		month=t.tm_mon
		day=t.tm_mday
		hour=t.tm_hour
		minute=t.tm_min
		sec=t.tm_sec

		wsname=str(month) + str(day) + " " + str(hour) + str(minute) + str(sec)

		ws=gui.Worksheet(wsname)
		event.Skip()
		
	
	def OnMenuSelection_Digits( self, event ): 
		event.Skip()


	def btnCalc_OnButtonClick( self, event ):
		PsyParams=dict()
		for Entry in self.m_Controls:
			if(Entry[0].GetValue()):
				if(Entry[1].GetValue()==""): 
					wx.MessageBox("A numeric value must be entered for " + Entry[2] + ".") 
					break
				else:
					PsyParams[Entry[3]] = float(Entry[1].GetValue())
		
		
		try:
			psy = eng.psychrometry(**PsyParams)
			result = psy.compute()

			for Entry in self.m_Controls:
				if(Entry[0].GetValue()):
					continue
				else:
					Entry[1].SetValue(str(getattr(result,Entry[3])))


			self.m_txtPw.SetValue(str(result.Pw))
			self.m_txtPws.SetValue(str(result.Pws))
			self.m_txtWs.SetValue(str(result.Ws))

		except Exception as e:
			wx.MessageBox(str(e))

		event.Skip()


if __name__=='__main__':
	frm=frmPsychrometry(None)
	frm.Show()

#app.MainLoop()
