import wx


class pnlRefrigerantSaturated ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 336,333 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizerLeft = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerLeft.AddGrowableCol( 1 )
		fgSizerLeft.SetFlexibleDirection( wx.BOTH )
		fgSizerLeft.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_radioT = wx.RadioButton( self, wx.ID_ANY, u"T (C)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioT, 0, wx.ALL, 5 )

		self.m_txtT = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioP = wx.RadioButton( self, wx.ID_ANY, u"P (kPa)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioP, 0, wx.ALL, 5 )

		self.m_txtP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVf = wx.RadioButton( self, wx.ID_ANY, u"vf (m3/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioVf, 0, wx.ALL, 5 )

		self.m_txtVf = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtVf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioVg = wx.RadioButton( self, wx.ID_ANY, u"vg (m3/kg)", wx.DefaultPosition, wx.DefaultSize, 0 )
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

		self.m_radioSf = wx.RadioButton( self, wx.ID_ANY, u"sf (kJ/kgK)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioSf, 0, wx.ALL, 5 )

		self.m_txtSf = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtSf, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioSg = wx.RadioButton( self, wx.ID_ANY, u"sg (kJ/kgK)", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_radioSg, 0, wx.ALL, 5 )

		self.m_txtHg = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerLeft.Add( self.m_txtHg, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 1, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute", wx.DefaultPosition, wx.DefaultSize, 0 )
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerandFit( mainSizer )
		self.Layout()

		# Connect Events
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


	# Virtual event handlers, overide them in your derived class
	def radioT_OnRadioButton( self, event ):
		event.Skip()

	def radioP_OnRadioButton( self, event ):
		event.Skip()

	def radioVf_OnRadioButton( self, event ):
		event.Skip()

	def radioVg_OnRadioButton( self, event ):
		event.Skip()

	def radioHf_OnRadioButton( self, event ):
		event.Skip()

	def radioHg_OnRadioButton( self, event ):
		event.Skip()

	def radioSf_OnRadioButton( self, event ):
		event.Skip()

	def radioSg_OnRadioButton( self, event ):
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		event.Skip()


