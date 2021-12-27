import wx

import scisuit.gui as gui
import scisuit.stats as stat


class frmtest_f ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"F Test")

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticVar1Range = wx.StaticText( self, wx.ID_ANY, u"Sample 1:")
		self.m_staticVar1Range.Wrap( -1 )

		fgSizer1.Add( self.m_staticVar1Range, 0, wx.ALL, 5 )

		self.m_txtVar1Range = gui.GridTextCtrl( self)
		fgSizer1.Add( self.m_txtVar1Range, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticVar2Range = wx.StaticText( self, wx.ID_ANY, u"Sample 2:")
		self.m_staticVar2Range.Wrap( -1 )

		fgSizer1.Add( self.m_staticVar2Range, 0, wx.ALL, 5 )

		self.m_txtVar2Range = gui.GridTextCtrl( self)
		fgSizer1.Add( self.m_txtVar2Range, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticMeanDiff = wx.StaticText( self, wx.ID_ANY, u"Assumed ratio:")
		self.m_staticMeanDiff.Wrap( -1 )

		fgSizer1.Add( self.m_staticMeanDiff, 0, wx.ALL, 5 )

		self.m_txtRatio = wx.TextCtrl( self, wx.ID_ANY, u"1.0")
		fgSizer1.Add( self.m_txtRatio, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticConfLevel = wx.StaticText( self, wx.ID_ANY, u"Confidence Level:")
		self.m_staticConfLevel.Wrap( -1 )

		fgSizer1.Add( self.m_staticConfLevel, 0, wx.ALL, 5 )

		self.m_txtConfLevel = wx.TextCtrl( self, wx.ID_ANY, u"95")
		fgSizer1.Add( self.m_txtConfLevel, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticAlternative = wx.StaticText( self, wx.ID_ANY, u"Alternative:")
		self.m_staticAlternative.Wrap( -1 )

		fgSizer1.Add( self.m_staticAlternative, 0, wx.ALL, 5 )

		Choices = [ u"less than", u"not equal", u"greater than" ]
		self.m_choiceAlternative = wx.Choice( self, choices = Choices)
		self.m_choiceAlternative.SetSelection( 1 )
		fgSizer1.Add( self.m_choiceAlternative, 0, wx.ALL, 5 )


		mainSizer.Add( fgSizer1, 0, wx.EXPAND, 5 )

		self.m_pnlOutput = wx.Panel( self)
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

		
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtnClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKBtnClick )


	def __del__( self ):
		pass

	
	def PrintValues(self, Vals:list, WS:gui.Worksheet, Row:int, Col:int):
		pval = Vals[0]
		Dict = Vals[1]
		Alternative = Vals[2]
		
		Header=["N", "Mean", "Std Dev", "SE Mean"]
		for j in range(len(Header)):
			WS[Row, Col + 1 + j] = Header[j] #+1 is for indentation
			
		Row += 1
		
		ListVals = [
			["Sample 1", Dict["N"], Dict["xaver"], Dict["s1"], Dict["s1"]/Dict["N"]],
			["Sample 2", Dict["N"], Dict["yaver"], Dict["s2"], Dict["s2"]/Dict["N"]],
			["Difference"," ", Dict["mean"], Dict["stdev"]],
			[None, None, None],
			["t-critical", Dict["tcritical"], None],
			["p-value", pval, None]]
		
			
		for List in ListVals:
			if(List[0] == None):
				Row += 1
				continue
				
			for i in range(len(List)):
				if(List[i] == None):
					continue
				WS[Row, Col + i] = List[i] 
			
			Row += 1
		

		WS[Row + 1, Col] = self.m_txtConfLevel.GetValue() + \
			"% Confidence Interval for " + \
			Alternative + \
			"(" + str(round(Dict["CI_lower"], 4)) + ", " + str(round(Dict["CI_upper"], 4)) + ")"
		
		return


	
	def OnCancelBtnClick( self, event ):
		self.Close()
		event.Skip()


	def OnOKBtnClick( self, event ):
		if(self.m_txtVar1Range.GetValue() == wx.EmptyString or
			self.m_txtVar2Range.GetValue() == wx.EmptyString):
			wx.MessageBox("Both ranges must be selected (variable 1 & 2).")
			return
		
		
		if(self.m_txtRatio.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for the assumed ratio.")
			return

		if(self.m_txtConfLevel.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for the confidence level.")
			return
		
		conflevel=float(self.m_txtConfLevel.GetValue())/100
		Ratio = float(self.m_txtRatio.GetValue())

		AlterOpt = ["less", "two.sided", "greater"]
		Alternative = AlterOpt[self.m_choiceAlternative.GetSelection()]

		xdata:list = gui.Range(self.m_txtVar1Range.GetValue()).tolist()
		ydata:list = gui.Range(self.m_txtVar2Range.GetValue()).tolist()
		

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
			pval, Dict = stat.test_f(x=xdata, 
				y=ydata,
				ratio = Ratio,
				alternative = Alternative, 
				conflevel = conflevel)
				
			Vals = [pval, Dict, Alternative]
		except Exception as e:
			wx.MessageBox(str(e))
			return
			
				
		self.PrintValues(Vals, WS, row, col)
		event.Skip()


