import wx

import scisuit.gui as gui


class frmFoodThermalProc ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent,title = u"Food Thermal Processing", size = wx.Size(-1, -1)) 

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticDTime = wx.StaticText( self, wx.ID_ANY, u"D (time):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticDTime.Wrap( -1 )

		fgSizer.Add( self.m_staticDTime, 0, wx.ALL, 5 )

		self.m_txtDTime = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer.Add( self.m_txtDTime, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"D (temperature):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		fgSizer.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.m_txtDTemperature = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer.Add( self.m_txtDTemperature, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"z-value:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		fgSizer.Add( self.m_staticText19, 0, wx.ALL, 5 )

		self.m_txtZ = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer.Add( self.m_txtZ, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Time:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		fgSizer.Add( self.m_staticText20, 0, wx.ALL, 5 )

		self.m_txtTime = gui.GridTextCtrl( self )
		fgSizer.Add( self.m_txtTime, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Temperature(s):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		fgSizer.Add( self.m_staticText21, 0, wx.ALL, 5 )

		self.m_txtTemperature = gui.GridTextCtrl( self )
		fgSizer.Add( self.m_txtTemperature, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Ref Temperature:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )

		fgSizer.Add( self.m_staticText23, 0, wx.ALL, 5 )

		self.m_txtRefTemperature = wx.TextCtrl( self, wx.ID_ANY,"121", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer.Add( self.m_txtRefTemperature, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizer, 1, wx.EXPAND, 5 )

		self.m_btnCalc = wx.Button( self, wx.ID_ANY, u"Calculate", wx.DefaultPosition, wx.DefaultSize, 0 )
		mainSizer.Add( self.m_btnCalc, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		self.m_btnCalc.Bind( wx.EVT_BUTTON, self.btnCalc_OnButtonClick )


	def btnCalc_OnButtonClick( self, event ):
		event.Skip()
    

if __name__ == "__main__":
	frm = frmFoodThermalProc(None) 
	frm.Show()

