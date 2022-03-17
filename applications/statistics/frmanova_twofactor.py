import os
import wx

import scisuit.gui as gui
import scisuit.stats as stat
import scisuit.util as util


class frmanova_twofactor ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent, title = u"Two-factor ANOVA")
		
		self.SetBackgroundColour( wx.Colour( 185, 185, 117 ) )
		
		ParentPath = util.parent_path(__file__)
		IconPath = ParentPath + os.sep + "images" + os.sep + "anova2factor.png"
		self.SetIcon(gui.makeicon(IconPath))


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

		Error = Dict["error"]
		Fact1 = Dict["fact1"]
		Fact2 = Dict["fact2"]
		Interact = Dict["interact"]
		
		Total_DF = Fact1["DF"]+Fact2["DF"]+Interact["DF"]+Error["DF"]
		Total_SS = Fact1["SS"]+Fact2["SS"]+Interact["SS"]+Error["SS"]

		ListVals = [
			["Factor #1", Fact1["DF"], Fact1["SS"] , Fact1["MS"], Fact1["F"], pval[0]],
			["Factor #2", Fact2["DF"], Fact2["SS"] , Fact2["MS"], Fact2["F"], pval[1]],
			["Interaction", Interact["DF"], Interact["SS"] , Interact["MS"], Interact["F"], pval[2]],
			[None],
			["Error", Error["DF"], Error["SS"] , Error["MS"]],
			[None],
			["Total", Total_DF , Total_SS]]
		
		
		for List in ListVals:
			if(List[0] == None):
				Row += 1
				continue
				
			for i in range(len(List)):
				WS[Row, Col+i] = List[i] 
				
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
		
		Response = gui.Range(self.m_txtResponse.GetValue()).tolist()
		Fact1 = gui.Range(self.m_txtFactor1.GetValue()).tolist() 
		Fact2 = gui.Range(self.m_txtFactor2.GetValue()).tolist() 
		
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
	frm = frmanova_twofactor(None)
	frm.Show()