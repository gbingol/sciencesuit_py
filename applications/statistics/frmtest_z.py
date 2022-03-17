import os
import wx

import scisuit.gui as gui
import scisuit.stats as stat
import scisuit.util as util


class frmtest_z ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Z Test")
		
		
		ParentPath = util.parent_path(__file__)
		IconPath = ParentPath + os.sep + "images" + os.sep + "test_z.png"
		self.SetIcon(gui.makeicon(IconPath))
		

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticVarRange = wx.StaticText( self, label = u"Variable Range:")
		self.m_staticVarRange.Wrap( -1 )

		fgSizer1.Add( self.m_staticVarRange, 0, wx.ALL, 5 )

		self.m_txtVarRange = gui.GridTextCtrl( self)
		fgSizer1.Add( self.m_txtVarRange, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTestMean = wx.StaticText( self, label = u"Test Mean:")
		self.m_staticTestMean.Wrap( -1 )

		fgSizer1.Add( self.m_staticTestMean, 0, wx.ALL, 5 )

		self.m_txtTestMean = wx.TextCtrl( self)
		fgSizer1.Add( self.m_txtTestMean, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticSigma = wx.StaticText( self, label = u"Sigma:")
		self.m_staticSigma.Wrap( -1 )

		fgSizer1.Add( self.m_staticSigma, 0, wx.ALL, 5 )

		self.m_txtSigma = wx.TextCtrl( self)
		fgSizer1.Add( self.m_txtSigma, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticConfLevel = wx.StaticText( self, label = u"Confidence Level:")
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

		self.m_pnlOutput = gui.pnlOutputOptions( self)
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
		
		Header=["N", "Average", "stdev", "SE Mean", "z", "p-value"]
		Vals =[Dict["N"], Dict["mean"], Dict["stdev"], Dict["SE"], Dict["zcritical"], pval] 
		for j in range(len(Header)):
			WS[Row, Col + j] = Header[j] 
			WS[Row + 1, Col + j] = Vals[j]
			
		Row += 2
		

		WS[Row + 1, Col] = self.m_txtConfLevel.GetValue() + \
			"% Confidence Interval for " + \
			Alternative + \
			"(" + str(round(Dict["CI_lower"], 4)) + ", " + str(round(Dict["CI_upper"], 4)) + ")"
		
		return

	
	def CheckInput(self):
		if(self.m_txtVarRange.GetValue() == wx.EmptyString):
			wx.MessageBox("Variable range cannot be blank.")
			return
		
		
		if(self.m_txtTestMean.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for the test mean.")
			return
		
		if(self.m_txtSigma.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for sigma.")
			return

		if(self.m_txtConfLevel.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for the confidence level.")
			return


	
	def OnCancelBtnClick( self, event ):
		self.Close()
		event.Skip()


	def OnOKBtnClick( self, event ):
		self.CheckInput()
		
		conflevel=float(self.m_txtConfLevel.GetValue())/100
		Mu = float(self.m_txtTestMean.GetValue())
		Sigma = float(self.m_txtSigma.GetValue()) #sd of population

		AlterOpt = ["less", "two.sided", "greater"]
		Alternative = AlterOpt[self.m_choiceAlternative.GetSelection()]

		xdata:list = gui.Range(self.m_txtVarRange.GetValue()).tolist()
		
		#output worksheet and top-left row and column
		WS, row, col = self.m_pnlOutput.Get()
		
		Vals=[]
		try:
			pval, Dict = stat.test_z(x=xdata, 
				mu = Mu,
				sd = Sigma,
				alternative = Alternative, 
				conflevel = conflevel)
				
			Vals = [pval, Dict, Alternative]
		except Exception as e:
			wx.MessageBox(str(e))
			return
			
				
		self.PrintValues(Vals, WS, row, col)
		event.Skip()


if __name__ == "__main__":
	frm = frmtest_z(None)
	frm.Show()


