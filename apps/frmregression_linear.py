import wx

import scisuit.gui as gui
import scisuit.stats as stat


class frmregression_linear ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Linear Regression")

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 208, 232, 232 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_lblResponse = wx.StaticText( self, label = u"Response:")
		self.m_lblResponse.Wrap( -1 )

		fgSizer.Add( self.m_lblResponse, 0, wx.ALL, 5 )

		self.m_txtResponse = gui.GridTextCtrl( self)
		fgSizer.Add( self.m_txtResponse, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblFactors = wx.StaticText( self, label = u"Factor(s):")
		self.m_lblFactors.Wrap( -1 )

		fgSizer.Add( self.m_lblFactors, 0, wx.ALL, 5 )

		self.m_txtFactors = gui.GridTextCtrl( self)
		fgSizer.Add( self.m_txtFactors, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblConfidence = wx.StaticText( self, label = u"Confidence Level:")
		self.m_lblConfidence.Wrap( -1 )

		fgSizer.Add( self.m_lblConfidence, 0, wx.ALL, 5 )

		self.m_txtConfidence = wx.TextCtrl( self, value = u"95")
		fgSizer.Add( self.m_txtConfidence, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkZeroIntercept = wx.CheckBox( self, label = u"intercept = 0")
		fgSizer.Add( self.m_chkZeroIntercept, 0, wx.ALL, 5 )


		fgSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		mainSizer.Add( fgSizer, 0, wx.EXPAND, 5 )

		self.m_chkStats = wx.CheckBox( self, label = u"Include stats (ANOVA, R2, table of coeffs)")
		self.m_chkStats.SetValue(True)
		mainSizer.Add( self.m_chkStats, 0, wx.ALL, 5 )

		self.m_pnlOutput = gui.pnlOutputOptions( self)
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


		self.m_chkZeroIntercept.Bind( wx.EVT_CHECKBOX, self.chkStacked_OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtnClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKBtnClick )



	def __del__( self ):
		pass


	
	def chkStacked_OnCheckBox( self, event ):
		event.Skip()

	def OnCancelBtnClick( self, event ):
		event.Skip()

	def OnOKBtnClick( self, event ):
		if(self.m_txtResponse.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for response.")
			return

		if(self.m_txtFactors.GetValue() == wx.EmptyString):
			wx.MessageBox("Factors range cannot be empty")
			return
		
		if(self.m_txtConfidence.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for response.")
			return

		conflevel = float(self.m_txtConfidence.GetValue())/100

		if(not (0<conflevel and conflevel<1)):
			wx.MessageBox("Confidence level must be in range (0, 100)")
			return
		
		Response = gui.Range(self.m_txtResponse.GetValue()).tolist()
		FactorsRng = gui.Range(self.m_txtFactors.GetValue())
		
		pvalue, Dict = None, None
		try:
			pvalue, Dict = stat.aov2(y=Response, x1 = Fact1, x2= Fact2)
		except Exception as e:
			wx.MessageBox(str(e))
			return
		
		WS, Row, Col = self.m_pnlOutput.Get()
		
		self.PrintValues([pvalue, Dict], WS, Row, Col)
		event.Skip()


if __name__ == "__main__":
	frm = frmregression_linear(None)
	frm.Show()