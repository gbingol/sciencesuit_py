import wx

app = wx.App()

class frmtestt_1sample ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, title = u"1-sample t-test")

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticVarRange = wx.StaticText( self, wx.ID_ANY, u"Variable Range:")
		self.m_staticVarRange.Wrap( -1 )

		fgSizer1.Add( self.m_staticVarRange, 0, wx.ALL, 5 )

		self.m_txtVarRange = wx.TextCtrl( self )
		fgSizer1.Add( self.m_txtVarRange, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTestMean = wx.StaticText( self, wx.ID_ANY, u"Test Mean:")
		self.m_staticTestMean.Wrap( -1 )

		fgSizer1.Add( self.m_staticTestMean, 0, wx.ALL, 5 )

		self.m_txtTestMean = wx.TextCtrl( self)
		fgSizer1.Add( self.m_txtTestMean, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticConfLevel = wx.StaticText( self, wx.ID_ANY, u"Confidence Level:" )
		self.m_staticConfLevel.Wrap( -1 )

		fgSizer1.Add( self.m_staticConfLevel, 0, wx.ALL, 5 )

		self.m_txtConfLevel = wx.TextCtrl( self, wx.ID_ANY, u"95" )
		fgSizer1.Add( self.m_txtConfLevel, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticAlternative = wx.StaticText( self, wx.ID_ANY, u"Alternative:")
		self.m_staticAlternative.Wrap( -1 )

		fgSizer1.Add( self.m_staticAlternative, 0, wx.ALL, 5 )

		m_choiceAlternativeChoices = [ u"less than", u"not equal", u"greater than" ]
		self.m_choiceAlternative = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceAlternativeChoices, 0)
		self.m_choiceAlternative.SetSelection( 1 )
		fgSizer1.Add( self.m_choiceAlternative, 0, wx.ALL, 5 )


		mainSizer.Add( fgSizer1, 0, wx.EXPAND, 5 )

		self.m_pnlOutput = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		mainSizer.Add( self.m_pnlOutput, 0, wx.ALL|wx.EXPAND, 5 )

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

		
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelButtonClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )

	def __del__( self ):
		pass


	
	def OnCancelButtonClick( self, event ):
		self.Close()
		event.Skip()


	def OnOKButtonClick( self, event ):
		if(self.m_txtVarRange.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for the variable.")
			return
		
		if(self.m_txtTestMean.GetValue() == wx.EmptyString):
			wx.MessagBox("A value must be entered for the test mean.")
			return
		
		conflevel=float(self.m_txtConfLevel.GetValue())/100
		Mu = float(self.m_txtTestMean.GetValue())

		InputRng = gui.Range(self.m_txtVarRange.GetValue())

		#output worksheet and top-left row and column
		WS = None
		row, col = 0, 0
		
		if(self.m_pnlOutput.IsNewWorksheet()):
			WS = gui.Worksheet()
		else:
			SelRange = self.m_pnlOutput.GetSelRange()
			WS = SelRange.parent()
			row, col = SelRange.coords()[0] #[0]:top-left

		
		event.Skip()


if __name__ == "__main__":
	frm =frmtestt_1sample(None)
	frm.Show()
	app.MainLoop()