import wx

import scisuit.gui as gui
import scisuit.stats as stat

class frmtestt_2sample ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Two-sample t-test")

		self.SetIcon(gui.makeicon("apps/images/t_test2sample.png"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticVar1Range = wx.StaticText( self, wx.ID_ANY, u"Variable 1 Range:")
		self.m_staticVar1Range.Wrap( -1 )

		fgSizer1.Add( self.m_staticVar1Range, 0, wx.ALL, 5 )

		self.m_txtVar1Range = gui.GridTextCtrl( self)
		fgSizer1.Add( self.m_txtVar1Range, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticVar2Range = wx.StaticText( self, wx.ID_ANY, u"Variable 2 Range:")
		self.m_staticVar2Range.Wrap( -1 )

		fgSizer1.Add( self.m_staticVar2Range, 0, wx.ALL, 5 )

		self.m_txtVar2Range = gui.GridTextCtrl( self)
		fgSizer1.Add( self.m_txtVar2Range, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticMeanDiff = wx.StaticText( self, wx.ID_ANY, u"Mean difference:")
		self.m_staticMeanDiff.Wrap( -1 )

		fgSizer1.Add( self.m_staticMeanDiff, 0, wx.ALL, 5 )

		self.m_txtMeanDiff = wx.TextCtrl( self, wx.ID_ANY, u"0.0")
		fgSizer1.Add( self.m_txtMeanDiff, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticConfLevel = wx.StaticText( self, wx.ID_ANY, u"Confidence Level:")
		self.m_staticConfLevel.Wrap( -1 )

		fgSizer1.Add( self.m_staticConfLevel, 0, wx.ALL, 5 )

		self.m_txtConfLevel = wx.TextCtrl( self, wx.ID_ANY, u"95")
		fgSizer1.Add( self.m_txtConfLevel, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticAlternative = wx.StaticText( self, wx.ID_ANY, u"Alternative:")
		self.m_staticAlternative.Wrap( -1 )

		fgSizer1.Add( self.m_staticAlternative, 0, wx.ALL, 5 )

		m_choiceAlternativeChoices = [ u"less than", u"not equal", u"greater than" ]
		self.m_choiceAlternative = wx.Choice( self, choices = m_choiceAlternativeChoices)
		self.m_choiceAlternative.SetSelection( 1 )
		fgSizer1.Add( self.m_choiceAlternative, 0, wx.ALL, 5 )

		self.m_chkSampleOneCol = wx.CheckBox( self, wx.ID_ANY, u"Sample in one column")
		fgSizer1.Add( self.m_chkSampleOneCol, 0, wx.ALL, 5 )

		self.m_chkEqualVar = wx.CheckBox( self, wx.ID_ANY, u"Assume equal variances")
		fgSizer1.Add( self.m_chkEqualVar, 0, wx.ALL, 5 )


		mainSizer.Add( fgSizer1, 0, wx.EXPAND, 5 )

		self.m_pnlOutput = gui.pnlOutputOptions( self )
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

		
		self.m_chkSampleOneCol.Bind( wx.EVT_CHECKBOX, self.chkSampleOneCol_OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelButtonClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )



	def __del__( self ):
		pass


	
	def chkSampleOneCol_OnCheckBox( self, event ):
		if(event.IsChecked() == True):
			self.m_staticVar1Range.SetLabel("Samples range:")
			self.m_staticVar2Range.SetLabel("Subscripts range:")
		else:
			self.m_staticVar1Range.SetLabel("Variable 1 Range:")
			self.m_staticVar2Range.SetLabel("Variable 2 Range:")

		event.Skip()


	def OnCancelButtonClick( self, event ):
		self.Close()
		event.Skip()

	
	def PrintValues(self, Vals:list, WS:gui.Worksheet, Row:int, Col:int):
		pval=Vals[0]
		Dict = Vals[1]
		Alternative = Vals[2]
		
		ListVals = [
			["Observation", Dict["n1"], Dict["n2"]],
			["Mean", Dict["xaver"], Dict["yaver"]],
			["Std Deviation", Dict["s1"], Dict["s2"]],
			[None, None, None],
			["t-critical", Dict["tcritical"], None],
			["p-value", pval, None]]
		
		if(self.m_chkEqualVar.GetValue()):
			ListVals.insert(3, ["Pooled variance", Dict["sp"], None])
			
		for List in ListVals:
			if(List[0] == None):
				Row += 1
				continue
				
			WS[Row, Col] = List[0] 
			WS[Row, Col+1]=List[1]
			
			if(List[2] != None):
				WS[Row, Col+2] = List[2]
			
			Row += 1
		

		WS[Row + 1, Col] = self.m_txtConfLevel.GetValue() + \
			"% Confidence Interval for " + \
			Alternative + \
			"(" + str(round(Dict["CI_lower"], 4)) + ", " + str(round(Dict["CI_upper"], 4)) + ")"
		
		return
		


	def OnOKButtonClick( self, event ):
		if(self.m_txtVar1Range.GetValue() == wx.EmptyString or
			self.m_txtVar2Range.GetValue() == wx.EmptyString):
			wx.MessageBox("Both ranges must be selected (variable 1 & 2).")
			return
		
		
		if(self.m_txtMeanDiff.GetValue() == wx.EmptyString):
			wx.MessagBox("A value must be entered for the assumed mean difference.")
			return
		
		conflevel=float(self.m_txtConfLevel.GetValue())/100
		MeanDiff = float(self.m_txtMeanDiff.GetValue())

		AlterOpt = ["less", "two.sided", "greater"]
		Alternative = AlterOpt[self.m_choiceAlternative.GetSelection()]

		var1:list = gui.Range(self.m_txtVar1Range.GetValue()).tolist()
		var2:list = gui.Range(self.m_txtVar2Range.GetValue()).tolist()

		xdata, ydata = [], []
		if(self.m_chkSampleOneCol.GetValue() == False):
			xdata = var1
			ydata = var2
		else:
			unique_subscripts = set(var2)
			
			if(len(unique_subscripts) > 2):
				raise RuntimeError("More than 2 types of samples exists")
			
			#convert to list for [] access
			unique_list = list(unique_subscripts)
			
			j = 0
			for elem in var1:
				subscript = var2[j]
				if(subscript == unique_list[0]):
					xdata.append(elem)
				else:
					ydata.append(elem)
				j += 1
			
		EqualVariances = self.m_chkEqualVar.GetValue()

		#output worksheet and top-left row and column
		WS = None
		row, col = 0, 0
		
		if(self.m_pnlOutput.IsNewWorksheet()):
			WS = gui.Worksheet()
		else:
			SelRange = self.m_pnlOutput.GetSelRange()
			WS = SelRange.parent()
			row, col = SelRange.coords()[0] #[0]:top-left
		
		Vals=[]
		try:
			pval, Dict = stat.test_t(x=xdata, 
				y=ydata,
				mu=MeanDiff, 
				varequal = EqualVariances, 
				alternative = Alternative, 
				conflevel = conflevel)
				
			Vals = [pval, Dict]
		except Exception as e:
			wx.MessageBox(str(e))
			return
		
		Vals.append(Alternative)
		self.PrintValues(Vals, WS, row, col)

		event.Skip()
		
		return


if __name__ == "__main__":
	frm = frmtestt_2sample(None)
	frm.Show()