import wx

import scisuit.gui as gui
import scisuit.stats as stat


class frmtest_sign ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Sign Test")

		self.SetIcon(gui.makeicon("apps/images/test_sign.png"))

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

		self.m_staticSample2 = wx.StaticText( self, label = u"Second Sample Range:")
		self.m_staticSample2.Wrap( -1 )

		self.m_staticSample2.Enable( False )

		fgSizer1.Add( self.m_staticSample2, 0, wx.ALL, 5 )

		self.m_txtSecondSample = gui.GridTextCtrl( self)
		self.m_txtSecondSample.Enable( False )

		fgSizer1.Add( self.m_txtSecondSample, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTestMedian = wx.StaticText( self, wx.ID_ANY, u"Test Median:")
		self.m_staticTestMedian.Wrap( -1 )

		fgSizer1.Add( self.m_staticTestMedian, 0, wx.ALL, 5 )

		self.m_txtMedian = wx.TextCtrl( self, wx.ID_ANY, u"0.0")
		fgSizer1.Add( self.m_txtMedian, 0, wx.ALL|wx.EXPAND, 5 )

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

		self.m_chkPaired = wx.CheckBox( self, wx.ID_ANY, u"Paired test")
		fgSizer1.Add( self.m_chkPaired, 0, wx.ALL, 5 )


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

		
		self.m_chkPaired.Bind( wx.EVT_CHECKBOX, self.chkPaired_OnCheckBox )
		self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.OnCancelButtonClick )
		self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )


	def __del__( self ):
		pass


	
	def chkPaired_OnCheckBox( self, event ):
		if(event.IsChecked() == True):
			self.m_staticVarRange.SetLabel("First sample range:")
		else:
			self.m_staticVarRange.SetLabel("Variable range:")
		
		self.m_staticSample2.Enable(event.IsChecked())
		self.m_txtSecondSample.Enable(event.IsChecked())
			
		event.Skip()


	def OnCancelButtonClick( self, event ):
		self.Close()
		event.Skip()

	def OnOKButtonClick( self, event ):
		if(self.m_txtVarRange.GetValue() == wx.EmptyString):
			wx.MessageBox("A range must be selected for variable 1.")
			return
		
		if(self.m_chkPaired.GetValue() == True and 
		self.m_txtSecondSample.GetValue == wx.EmptyString):
			wx.MessageBox("A range must be selected for second sample.")
			return
		
		conflevel=float(self.m_txtConfLevel.GetValue())/100
		AssumedMedian = float(self.m_txtMedian.GetValue())
		ComputedMedian = None 

		SelIndex = self.m_choiceAlternative.GetSelection()
		Alternative = (["less", "two.sided", "greater"])[SelIndex]
		AlternativeSign = (["<", "!=", ">"])[SelIndex]
		
		
		var1:list = gui.Range(self.m_txtVar1Range.GetValue()).tolist()
		ComputedMedian = stat.median(var1)
		var2 = []
		if(self.m_chkPaired.GetValue()):
			var2 = gui.Range(self.m_txtVar2Range.GetValue()).tolist()
			if(len(var1) != len(var2)):
				wx.MessageBox("If paired test is selected, then both variables must be of same size.")
				return
			
			diffList = []
			for i in range(len(var1)):
				diffList.append(var1[i]-var2[i])
			ComputedMedian = stat.median(diffList)
		
		WS, row, col = self.m_pnlOutput.Get()

		Median = None
		pvalue, Dict = None, None



		event.Skip()


