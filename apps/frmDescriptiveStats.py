import wx

app = wx.App()

class frmDescriptiveStats ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Descriptive Statistics", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 255, 192, 130 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		inputSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticTxtInput = wx.StaticText( self, wx.ID_ANY, u"Input:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtInput.Wrap( -1 )

		inputSizer.Add( self.m_staticTxtInput, 0, wx.ALL, 5 )

		self.m_txtInput = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		inputSizer.Add( self.m_txtInput, 1, wx.ALL, 5 )


		mainSizer.Add( inputSizer, 0, wx.EXPAND, 5 )

		self.m_chkTreatCols = wx.CheckBox( self, wx.ID_ANY, u"Treat columns separately", wx.DefaultPosition, wx.DefaultSize, 0 )
		mainSizer.Add( self.m_chkTreatCols, 0, wx.ALL, 5 )

		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_chkAll = wx.CheckBox( self, wx.ID_ANY, u"All", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkAll, 0, wx.ALL, 5 )

		self.m_chkCount = wx.CheckBox( self, wx.ID_ANY, u"count", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkCount, 1, wx.ALL, 5 )

		self.m_chkKurtosis = wx.CheckBox( self, wx.ID_ANY, u"kurtosis", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkKurtosis, 0, wx.ALL, 5 )

		self.m_chkMin = wx.CheckBox( self, wx.ID_ANY, u"min", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkMin, 0, wx.ALL, 5 )

		self.m_chkMean = wx.CheckBox( self, wx.ID_ANY, u"mean", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkMean, 0, wx.ALL, 5 )

		self.m_chkMedian = wx.CheckBox( self, wx.ID_ANY, u"median", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkMedian, 0, wx.ALL, 5 )

		self.m_chkMax = wx.CheckBox( self, wx.ID_ANY, u"max", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkMax, 0, wx.ALL, 5 )

		self.m_chkMode = wx.CheckBox( self, wx.ID_ANY, u"mode", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkMode, 0, wx.ALL, 5 )

		self.m_chkRange = wx.CheckBox( self, wx.ID_ANY, u"range", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkRange, 0, wx.ALL, 5 )

		self.m_chkVar = wx.CheckBox( self, wx.ID_ANY, u"variance", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkVar, 0, wx.ALL, 5 )

		self.m_chkSD = wx.CheckBox( self, wx.ID_ANY, u"standard dev", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkSD, 0, wx.ALL, 5 )

		self.m_chkSE = wx.CheckBox( self, wx.ID_ANY, u"standard error", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkSE, 0, wx.ALL, 5 )

		self.m_chkSum = wx.CheckBox( self, wx.ID_ANY, u"sum", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkSum, 0, wx.ALL, 5 )

		self.m_chkSkewness = wx.CheckBox( self, wx.ID_ANY, u"skewness", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_chkSkewness, 0, wx.ALL, 5 )


		mainSizer.Add( fgSizer1, 0, wx.EXPAND, 5 )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		mainSizer.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer = wx.StdDialogButtonSizer()
		self.m_sdbSizerOK = wx.Button( self, wx.ID_OK )
		m_sdbSizer.AddButton( self.m_sdbSizerOK )
		self.m_sdbSizerCancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer.AddButton( self.m_sdbSizerCancel )
		m_sdbSizer.Realize()

		mainSizer.Add( m_sdbSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		self.m_Controls =[
			self.m_chkCount, self.m_chkKurtosis, self.m_chkMax, self.m_chkMean, self.m_chkMedian,
			self.m_chkMin, self.m_chkMode, self.m_chkRange, self.m_chkSD, self.m_chkSE,
			self.m_chkSkewness, self.m_chkSum, self.m_chkVar
		]

		# Connect Events
		self.m_chkAll.Bind( wx.EVT_CHECKBOX, self.chkAll_OnCheck )
		self.m_chkCount.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkKurtosis.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkMin.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkMean.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkMedian.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkMax.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkMode.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkRange.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkVar.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkSD.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkSE.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkSum.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_chkSkewness.Bind( wx.EVT_CHECKBOX, self.OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelButton )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKButton )

	def __del__( self ):
		pass


	def chkAll_OnCheck( self, event ):
		for chk in self.m_Controls:
			chk.SetValue(event.IsChecked())

	def OnCheckBox( self, event ):
		#if any is unchecked then All must be unchecked
		if(event.IsChecked() == False):
			self.m_chkAll.SetValue(False)
		else:
			#if all checkboxes are checked then check chkAll
			for chk in self.m_Controls:
				if(chk.GetValue() == False):
					return
			self.m_chkAll.SetValue(True)


	def OnCancelButton( self, event ):
		frm.Close()
		event.Skip()

	def OnOKButton( self, event ):
		event.Skip()


if __name__=="__main__":
	frm = frmDescriptiveStats(None)
	frm.Show()
	app.MainLoop()