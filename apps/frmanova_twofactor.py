import wx

import scisuit.gui as gui
import scisuit.stats as stat



class frmanova_twofactor ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Two-factor ANOVA")
		
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )
		self.SetIcon(gui.makeicon("apps/images/anova2factor.png"))


		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

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

		self.m_lblFactor1 = wx.StaticText( self, label = u"Factor 1:")
		self.m_lblFactor1.Wrap( -1 )

		fgSizer.Add( self.m_lblFactor1, 0, wx.ALL, 5 )

		self.m_txtFactor1 = gui.GridTextCtrl( self)
		fgSizer.Add( self.m_txtFactor1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblFactor2 = wx.StaticText( self, label = u"Factor 2:")
		self.m_lblFactor2.Wrap( -1 )

		fgSizer.Add( self.m_lblFactor2, 0, wx.ALL, 5 )

		self.m_txtFactor2 = gui.GridTextCtrl( self)
		fgSizer.Add( self.m_txtFactor2, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblConfidence = wx.StaticText( self, label = u"Confidence Level:")
		self.m_lblConfidence.Wrap( -1 )

		fgSizer.Add( self.m_lblConfidence, 0, wx.ALL, 5 )

		self.m_txtConfidence = wx.TextCtrl( self, value = u"95")
		fgSizer.Add( self.m_txtConfidence, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizer, 0, wx.EXPAND, 5 )

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

		# Connect Events
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtnClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKBtnClick )



	def __del__( self ):
		pass



	def OnCancelBtnClick( self, event ):
		self.Close()
		event.Skip()
	


	def PrintValues(self, Vals:list, WS:gui.Worksheet, Row:int, Col:int):
		pval=Vals[0]
		Dict = Vals[1]
		

		Headers = [ "Source", "df","SS", "MS","F-value", "p-value"]
		for i in range(len(Headers)):
			WS[Row, Col + i] = Headers[i]
		
		Row += 1

		Treatment = Dict["Treatment"]
		Error = Dict["Error"]
		Total = Dict["Total"]

		ListVals = [
			["Treatment", Treatment["DF"], Treatment["SS"] , Treatment["MS"], Dict["Fvalue"], pval],
			["Error", Error["DF"], Error["SS"] , Error["MS"]],
			["Total", Total["DF"], Total["SS"] , Total["MS"]]]
		
		
		for List in ListVals:
			for i in range(len(List)):
				WS[Row, Col+i] = List[i] 
			Row += 1
		
		Row += 1
		
		if(Tukey != None):
			Headers = ["Pairwise Diff", "Difference (i-j)", "Tukey Interval"]
			for i  in range(len(Headers)):
				WS[Row, Col+i] = Headers[i] 
				
			Row += 1
			
			for CompCls in Tukey:
				WS[Row, Col] = str(CompCls.m_a + 1) + "-" + str(CompCls.m_b + 1)
				WS[Row, Col + 1] = str(round(CompCls.m_MeanValueDiff, 2))
				WS[Row, Col + 2] = str(round(CompCls.m_CILow, 2)) + ", " + str(round(CompCls.m_CIHigh, 2))
				
				Row += 1
		
		return


	def OnOKBtnClick( self, event ):
		if(self.m_txtResponse.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for response.")
			return

		if(self.m_txtFactor1.GetValue() == wx.EmptyString or 
			self.m_txtFactor2.GetValue() == wx.EmptyString):
			wx.MessageBox("Factors range cannot be empty, a selection must be made")
			return
		
		if(self.m_txtConfidence.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for response.")
			return
		
		conflevel=float(self.m_txtConfidence.GetValue())/100
		Alpha = 1 - conflevel

		if(not(0<Alpha and Alpha<1)):
			wx.MessageBox("Confidence level must be between (0, 100)")
			return

		event.Skip()


if __name__ == "__main__":
	frm = frmanova_twofactor(None)
	frm.Show()