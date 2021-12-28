import wx

app = wx.App()


class frmanova_singlefactor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, title = u"One-Way ANOVA")

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_lblResponses = wx.StaticText( self, wx.ID_ANY, u"Response Variables Range:")
		self.m_lblResponses.Wrap( -1 )

		fgSizer.Add( self.m_lblResponses, 0, wx.ALL, 5 )

		self.m_txtResponses = wx.TextCtrl( self)
		fgSizer.Add( self.m_txtResponses, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblFactors = wx.StaticText( self, wx.ID_ANY, u"Factors:")
		self.m_lblFactors.Wrap( -1 )

		self.m_lblFactors.Enable( False )

		fgSizer.Add( self.m_lblFactors, 0, wx.ALL, 5 )

		self.m_txtFactors = wx.TextCtrl( self)
		self.m_txtFactors.Enable( False )

		fgSizer.Add( self.m_txtFactors, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblConfidence = wx.StaticText( self, wx.ID_ANY, u"Confidence Level:")
		self.m_lblConfidence.Wrap( -1 )

		fgSizer.Add( self.m_lblConfidence, 0, wx.ALL, 5 )

		self.m_txtConfidence = wx.TextCtrl( self, wx.ID_ANY, u"95")
		fgSizer.Add( self.m_txtConfidence, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkStacked = wx.CheckBox( self, wx.ID_ANY, u"My data is stacked")
		fgSizer.Add( self.m_chkStacked, 0, wx.ALL, 5 )


		fgSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_chkTukeyTest = wx.CheckBox( self, wx.ID_ANY, u"Tukey's Test")
		self.m_chkTukeyTest.SetValue(True)
		fgSizer.Add( self.m_chkTukeyTest, 0, wx.ALL, 5 )


		fgSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		mainSizer.Add( fgSizer, 0, wx.EXPAND, 5 )

		self.m_pnlOutput = wx.Panel( self)
		mainSizer.Add( self.m_pnlOutput, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer = wx.StdDialogButtonSizer()
		self.m_sdbSizerOK = wx.Button( self, wx.ID_OK )
		m_sdbSizer.AddButton( self.m_sdbSizerOK )
		self.m_sdbSizerCancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer.AddButton( self.m_sdbSizerCancel )
		m_sdbSizer.Realize()

		mainSizer.Add( m_sdbSizer, 0, wx.EXPAND, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		
		self.m_chkStacked.Bind( wx.EVT_CHECKBOX, self.chkStacked_OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtnClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKBtnClick )


	def __del__( self ):
		pass


	
	def chkStacked_OnCheckBox( self, event ):
		if(event.IsChecked() == True):
			self.m_lblResponses.SetLabel("Response Variable Range:")
		else:
			self.m_lblResponses.SetLabel("Response Variables Range:")
		
		self.m_lblFactors.Enable(event.IsChecked())
		self.m_txtFactors.Enable(event.IsChecked())
		event.Skip()


	def OnCancelBtnClick( self, event ):
		self.Close()
		event.Skip()
		

	def OnOKBtnClick( self, event ):
		event.Skip()


if __name__ == "__main__":
	frm = frmanova_singlefactor(None)
	frm.Show()

	app.MainLoop()