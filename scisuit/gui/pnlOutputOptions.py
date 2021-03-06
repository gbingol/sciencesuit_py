import wx

import scisuit.gui as gui


class pnlOutputOptions ( wx.Panel ):

	def __init__( self, parent, bgcolor = None):
		wx.Panel.__init__ ( self, parent)

		#imitate parent's background color to blend well
		if(bgcolor == None):
			self.SetBackgroundColour(parent.GetBackgroundColour())
		else:
			if(isinstance(bgcolor, wx.Colour) == False):
				raise TypeError("bgcolor must be of type wx.Colour")
			self.SetBackgroundColour(bgcolor)

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		#header section
		sizerHeader = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText = wx.StaticText( self, wx.ID_ANY, u"Ouput Options" )
		self.m_staticText.Wrap( -1 )

		sizerHeader.Add( self.m_staticText, 0, wx.ALL, 5 )
		self.m_staticlineHeader = wx.StaticLine( self )
		sizerHeader.Add( self.m_staticlineHeader, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		mainSizer.Add( sizerHeader, 0, wx.EXPAND, 5 )


		#selection section
		fgSizer = wx.FlexGridSizer( 0, 2, 10, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_radioSelection = wx.RadioButton( self, wx.ID_ANY, u"Selection")
		fgSizer.Add( self.m_radioSelection, 0, wx.ALL, 5 )

		self.m_txtSelRange = gui.GridTextCtrl( self)
		self.m_txtSelRange.Enable(False) #radiobox is selected, so disable it
		fgSizer.Add( self.m_txtSelRange, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioNewWS = wx.RadioButton( self, wx.ID_ANY, u"New Sheet")
		self.m_radioNewWS.SetValue( True ) #by default new worksheet
		fgSizer.Add( self.m_radioNewWS, 0, wx.ALL, 5 )

		mainSizer.Add( fgSizer, 0, wx.EXPAND, 5 )


		#footer section
		sizerFooter = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticlineFooter = wx.StaticLine( self)
		sizerFooter.Add( self.m_staticlineFooter, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		mainSizer.Add( sizerFooter, 0, wx.EXPAND, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()


		self.m_radioSelection.Bind( wx.EVT_RADIOBUTTON, self.radioSelection_OnRadioBtn )
		self.m_radioNewWS.Bind( wx.EVT_RADIOBUTTON, self.radioNewWS_OnRadioBtn )

	def __del__( self ):
		pass


	def radioSelection_OnRadioBtn( self, event ):
		self.m_txtSelRange.Enable()
		event.Skip()

	def radioNewWS_OnRadioBtn( self, event ):
		self.m_txtSelRange.Enable(False)
		event.Skip()
	
	def GetSelRangeText(self):
		"""
		returns the range as text
		"""
		return self.m_txtSelRange.GetValue()

	def GetSelRange(self):
		if(self.m_radioSelection.GetValue() == True and self.GetSelRangeText() != wx.EmptyString):
			return gui.Range(self.GetSelRangeText())


	def IsNewWorksheet(self):
		return self.m_radioNewWS.GetValue()
	
	def IsSelRange(self):
		return self.m_radioSelection.GetValue()
	

	def Get(self)->tuple:
		WS = None
		row, col = 0, 0
		
		if(self.IsNewWorksheet()):
			WS = gui.Worksheet()
		else:
			SelRange = self.GetSelRange()
			WS = SelRange.parent()
			row, col = SelRange.coords()[0] #[0]:top-left
		
		return WS, row, col

