import wx

import scisuit.gui as gui
import scisuit.stats as stat


class frmanova_singlefactor ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"One-Way ANOVA")
		
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )
		self.SetIcon(gui.makeicon("apps/images/anovasinglefactor.png"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_lblResponses = wx.StaticText( self, label = u"Response Variables Range:")
		self.m_lblResponses.Wrap( -1 )

		fgSizer.Add( self.m_lblResponses, 0, wx.ALL, 5 )

		self.m_txtResponses = gui.GridTextCtrl( self)
		fgSizer.Add( self.m_txtResponses, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblFactors = wx.StaticText( self, label = u"Factors:")
		self.m_lblFactors.Wrap( -1 )

		self.m_lblFactors.Enable( False )

		fgSizer.Add( self.m_lblFactors, 0, wx.ALL, 5 )

		self.m_txtFactors = gui.GridTextCtrl( self)
		self.m_txtFactors.Enable( False )

		fgSizer.Add( self.m_txtFactors, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_lblConfidence = wx.StaticText( self, label = u"Confidence Level:")
		self.m_lblConfidence.Wrap( -1 )

		fgSizer.Add( self.m_lblConfidence, 0, wx.ALL, 5 )

		self.m_txtConfidence = wx.TextCtrl( self, value = u"95")
		fgSizer.Add( self.m_txtConfidence, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chkStacked = wx.CheckBox( self, label = u"My data is stacked")
		fgSizer.Add( self.m_chkStacked, 0, wx.ALL, 5 )


		fgSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_chkTukeyTest = wx.CheckBox( self, label = u"Tukey's Test")
		self.m_chkTukeyTest.SetValue(True)
		fgSizer.Add( self.m_chkTukeyTest, 0, wx.ALL, 5 )


		fgSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )


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

		
		self.m_chkStacked.Bind( wx.EVT_CHECKBOX, self.chkStacked_OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtnClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKBtnClick )


	def __del__( self ):
		pass


	
	def chkStacked_OnCheckBox( self, event ):
		"""
		If stacked, dont perform Tukey test since 
		Pairwise Diff and Difference columns in Tukey test refer to random 
		values in the stacked factors (utterly confusing)
		
		A remedy would be to sort the values in the UniqueList variable but
		the clearer one is to let user to unstack
		"""
		if(event.IsChecked() == True):
			self.m_lblResponses.SetLabel("Response Variable Range:")
			self.m_chkTukeyTest.SetValue(False)
		else:
			self.m_lblResponses.SetLabel("Response Variables Range:")
		
		self.m_lblFactors.Enable(event.IsChecked())
		self.m_txtFactors.Enable(event.IsChecked())
		
		self.m_chkTukeyTest.Enable(not event.IsChecked())
		
		event.Skip()


	def OnCancelBtnClick( self, event ):
		self.Close()
		event.Skip()

	
	def PrintValues(self, Vals:list, WS:gui.Worksheet, Row:int, Col:int):
		pval=Vals[0]
		Dict = Vals[1]
		Tukey = Vals[2]

		Headers = [ "Source", "df","SS", "MS","F", "P"]
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
		IsStacked: bool = self.m_chkStacked.GetValue()
		
		if(self.m_txtResponses.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for response.")
			return

		if(IsStacked and self.m_txtFactors.GetValue() == wx.EmptyString):
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
		
		Responses = []

		rngResponses = gui.Range(self.m_txtResponses.GetValue())
		ResponseList = rngResponses.tolist()
		if(not IsStacked):
			for i in range(rngResponses.ncols()):
				subRng = rngResponses.subrange(row=0, col=i, nrows = -1, ncols = 1)
				Responses.append(subRng.tolist())
		else:
			rngFactors=gui.Range(self.m_txtFactors.GetValue())
			if(rngResponses.ncols() > 1 or rngFactors.ncols() > 1):
				wx.MessageBox("The factors or the responses must be in a single column")
				return
			ListFactors = rngFactors.tolist()
			FactorsSet = set(ListFactors)
			UniqueFactors = list(FactorsSet)
			
			for i in range(len(UniqueFactors)):
				Responses.append([])
			
			for i in range(len(ListFactors)):
				for j in range(len(UniqueFactors)):
					if(ListFactors[i] == UniqueFactors[j]):
						Responses[j].append(ResponseList[i])
						break


		pvalue, dic, TukeyList = None, None, None
		try:
			cls = stat.aov(*Responses)
			pvalue, dic = cls.compute()
			if(self.m_chkTukeyTest.GetValue()):
				TukeyList = cls.tukey(Alpha)

		except Exception as e:
			wx.MessageBox(str(e))
			return
		
		WS, row, col = self.m_pnlOutput.Get()

		self.PrintValues([pvalue, dic, TukeyList], WS, row, col)

		event.Skip()


if __name__ == "__main__":
	frm = frmanova_singlefactor(None)
	frm.Show()