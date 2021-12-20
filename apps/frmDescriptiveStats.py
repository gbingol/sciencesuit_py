import wx

import math
import numbers

import scisuit.core as scr
import scisuit.gui as gui
import scisuit.stats as stat



def _basicstat(v):
	Min, Max = float('inf'), float('-inf')
	N = 0
	Sum = 0
	for elem in v:
		if(isinstance(elem, numbers.Real) == False):
			continue
		Min = Min if Min<=elem else elem
		Max = Max if elem<=Max else elem
		Sum += elem
		N += 1

	if(N == 0):
		raise ValueError("No real numbers are present in the selection")

	return {'Min':Min, 'Max':Max, 'Range':Max-Min, 'Sum': Sum, 'Count':N, 'Mean': Sum / N} 


def _Moment(v):
	variance = stats.var(v)
	sd = math.sqrt(variance)
	se = sd / math.sqrt(len(v))

	return {'Var':variance, 'SD':sd, 'SE':se}




class frmDescriptiveStats ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Descriptive Statistics", )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 255, 192, 130 ) )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		#input range section
		inputSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticTxtInput = wx.StaticText( self, wx.ID_ANY, u"Input:")
		self.m_staticTxtInput.Wrap( -1 )

		inputSizer.Add( self.m_staticTxtInput, 0, wx.ALL, 5 )

		self.m_txtInput = gui.GridTextCtrl( self)
		inputSizer.Add( self.m_txtInput, 1, wx.ALL, 5 )


		mainSizer.Add( inputSizer, 0, wx.EXPAND, 5 )


		#whether to treat columns separately or as whole
		self.m_chkTreatCols = wx.CheckBox( self, wx.ID_ANY, u"Treat columns separately" )
		mainSizer.Add( self.m_chkTreatCols, 0, wx.ALL, 5 )

		fgSizer = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_chkAll = wx.CheckBox( self, wx.ID_ANY, u"All")
		fgSizer.Add( self.m_chkAll, 0, wx.ALL, 5 )

		self.m_chkCount = wx.CheckBox( self, wx.ID_ANY, u"count")
		fgSizer.Add( self.m_chkCount, 1, wx.ALL, 5 )

		self.m_chkKurtosis = wx.CheckBox( self, wx.ID_ANY, u"kurtosis")
		fgSizer.Add( self.m_chkKurtosis, 0, wx.ALL, 5 )

		self.m_chkMin = wx.CheckBox( self, wx.ID_ANY, u"min")
		fgSizer.Add( self.m_chkMin, 0, wx.ALL, 5 )

		self.m_chkMean = wx.CheckBox( self, wx.ID_ANY, u"mean")
		fgSizer.Add( self.m_chkMean, 0, wx.ALL, 5 )

		self.m_chkMedian = wx.CheckBox( self, wx.ID_ANY, u"median")
		fgSizer.Add( self.m_chkMedian, 0, wx.ALL, 5 )

		self.m_chkMax = wx.CheckBox( self, wx.ID_ANY, u"max")
		fgSizer.Add( self.m_chkMax, 0, wx.ALL, 5 )

		self.m_chkMode = wx.CheckBox( self, wx.ID_ANY, u"mode")
		fgSizer.Add( self.m_chkMode, 0, wx.ALL, 5 )

		self.m_chkRange = wx.CheckBox( self, wx.ID_ANY, u"range")  
		fgSizer.Add( self.m_chkRange, 0, wx.ALL, 5 )

		self.m_chkVar = wx.CheckBox( self, wx.ID_ANY, u"variance")  
		fgSizer.Add( self.m_chkVar, 0, wx.ALL, 5 )

		self.m_chkSD = wx.CheckBox( self, wx.ID_ANY, u"standard dev")
		fgSizer.Add( self.m_chkSD, 0, wx.ALL, 5 )

		self.m_chkSE = wx.CheckBox( self, wx.ID_ANY, u"standard error")
		fgSizer.Add( self.m_chkSE, 0, wx.ALL, 5 )

		self.m_chkSum = wx.CheckBox( self, wx.ID_ANY, u"sum")
		fgSizer.Add( self.m_chkSum, 0, wx.ALL, 5 )

		self.m_chkSkewness = wx.CheckBox( self, wx.ID_ANY, u"skewness")
		fgSizer.Add( self.m_chkSkewness, 0, wx.ALL, 5 )

 
		mainSizer.Add( fgSizer, 0, wx.EXPAND, 5 )

		self.m_pnlOutput = gui.pnlOutputOptions( self )
		mainSizer.Add( self.m_pnlOutput, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer = wx.StdDialogButtonSizer()
		self.m_sdbSizerOK = wx.Button( self, wx.ID_OK )
		m_sdbSizer.AddButton( self.m_sdbSizerOK )
		self.m_sdbSizerCancel = wx.Button( self, wx.ID_CANCEL ) 
		m_sdbSizer.AddButton( self.m_sdbSizerCancel ) 
		m_sdbSizer.Realize()

		mainSizer.Add( m_sdbSizer, 1, wx.EXPAND, 5 )   

 
		self.SetSizerAndFit( mainSizer )
		self.Layout() 

		self.Centre( wx.BOTH )  

		self.m_Controls =[   
			[self.m_chkCount, _basicstat, "Count"] ,
			[self.m_chkKurtosis, _Moment, "Kurtosis"], 
			[self.m_chkMax,_basicstat, "Max"], 
			[self.m_chkMean,_basicstat, "Mean"],
			[self.m_chkMedian,stat.median, "Median"],  
			[self.m_chkMin,_basicstat, "Min"], 
			[self.m_chkMode, stat.mode, "Mode"],  
			[self.m_chkRange,_basicstat, "Range"], 
			[self.m_chkSD, _Moment, "SD"],
			[self.m_chkSE, _Moment, "SE"], 
			[self.m_chkSkewness, stat.skew, "Skewness"], 
			[self.m_chkSum, _basicstat, "Sum"],
			[self.m_chkVar, stat.var, "Variance"]] 


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
				if(chk[0].GetValue() == False):
					return
			self.m_chkAll.SetValue(True)


	def OnCancelButton( self, event ):
		frm.Close()
		event.Skip()

	def OnOKButton( self, event ):
		if(self.m_staticTxtInput.GetValue() == wx.EmptyString):
			wx.MessageBox("A data range must be selected")
			return
		
		InputRng = gui.Range(self.m_staticTxtInput.GetValue())
		OutputTarget = None
		
		if(self.m_pnlOutput.IsNewWorksheet()):
			OutputTarget = gui.Worksheet()
		else:
			OutputTarget = self.m_pnlOutput.GetSelRange()
		
		row, col = 0, 0
		
		Dict = dict() #initial empty dict 
		for Ctrl in self.m_Controls:
			if(Ctrl[0].GetValue() == False): #unchecked
				continue

			func, Name = Ctrl[1], Ctrl[2]
			
		
		event.Skip()





if __name__=="__main__":
	frm = frmDescriptiveStats(None)
	frm.Show()