import wx

import scisuit.core as scr
import scisuit.gui as gui
import scisuit.integrate as integ



def FindAvg(vec):
	retVec=scr.Vector(0)
	
	for i in range(1, len(vec)):
		avg=(vec[i]+vec[i-1])/2.0
		retVec.pushback(avg)

	return retVec 




class frmFoodThermalProc ( gui.Frame ):

	def __init__( self, parent ):
		gui.Frame.__init__ ( self, parent,title = u"Food Thermal Processing", size = wx.Size(-1, -1)) 
		
		self.SetBackgroundColour( wx.Colour( 255, 199, 142 ) )
		
		self.SetIcon(gui.makeicon("applications/engineering/images/thermalprocessing.jpg"))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		fgSizer = wx.FlexGridSizer( 0, 2, 5, 0 )
		fgSizer.AddGrowableCol( 1 )
		fgSizer.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticDTime = wx.StaticText( self, wx.ID_ANY, u"D (time):")
		self.m_staticDTime.Wrap( -1 )

		fgSizer.Add( self.m_staticDTime, 0, wx.ALL, 5 )

		self.m_txtDTime = wx.TextCtrl( self)
		fgSizer.Add( self.m_txtDTime, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"D (temperature):")
		self.m_staticText18.Wrap( -1 )

		fgSizer.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.m_txtDTemperature = wx.TextCtrl( self)
		fgSizer.Add( self.m_txtDTemperature, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"z-value:")
		self.m_staticText19.Wrap( -1 )

		fgSizer.Add( self.m_staticText19, 0, wx.ALL, 5 )

		self.m_txtZ = wx.TextCtrl( self)
		fgSizer.Add( self.m_txtZ, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Time:")
		self.m_staticText20.Wrap( -1 )

		fgSizer.Add( self.m_staticText20, 0, wx.ALL, 5 )

		self.m_txtTime = gui.GridTextCtrl( self )
		fgSizer.Add( self.m_txtTime, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Temperature(s):")
		self.m_staticText21.Wrap( -1 )

		fgSizer.Add( self.m_staticText21, 0, wx.ALL, 5 )

		self.m_txtTemperature = gui.GridTextCtrl( self )
		fgSizer.Add( self.m_txtTemperature, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Ref Temperature:")
		self.m_staticText23.Wrap( -1 )

		fgSizer.Add( self.m_staticText23, 0, wx.ALL, 5 )

		self.m_txtRefTemperature = wx.TextCtrl( self, wx.ID_ANY,"121")
		fgSizer.Add( self.m_txtRefTemperature, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizer, 1, wx.EXPAND, 5 )

		self.m_btnCalc = wx.Button( self, wx.ID_ANY, u"Calculate")
		mainSizer.Add( self.m_btnCalc, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		self.m_btnCalc.Bind( wx.EVT_BUTTON, self.btnCalc_OnButtonClick )
	
	


	def btnCalc_OnButtonClick( self, event ):
		
		if(self.m_txtZ.GetValue() == wx.EmptyString):
			wx.MessageBox("A valid number must be entered for z-value")
			return
		
		if(self.m_txtDTemperature.GetValue() == wx.EmptyString):
			wx.MessageBox("A valid number must be entered for D(Temperature)")
			return
		
		if(self.m_txtDTime.GetValue() == wx.EmptyString):
			wx.MessageBox("A valid number must be entered for D(time)")
			return
		
		zvalue = float(self.m_txtZ.GetValue())
		Dvalue_Temp, Dvalue_Time=float(self.m_txtDTemperature.GetValue()) , float(self.m_txtDTime.GetValue())
		RefTemp=float(self.m_txtRefTemperature.GetValue())
		
		if(Dvalue_Time<=0 or  zvalue<=0) : 
			wx.MessageBox("Neither D-value nor z-value can not be smaller or equal to zero") 
			return 
		
		
		WS=gui.Worksheet()
		
		def Compute(Time, Temperature, Row, Col, CurTemperatureRangeInfo = None):
			if(len(Time) != len(Temperature)):
				wx.MessageBox("The length of time and temperature data are not equal.")
				return
			
			DValue = Dvalue_Time*10.0**((Dvalue_Temp-Temperature)/zvalue) #vector
			LethalRate=10.0**((Temperature-RefTemp)/zvalue) #vector
			FValue=integ.cumtrapz_d(x=Time, y=LethalRate) #returns a vector
			
			dt=scr.diff(Time)
			avg_T=FindAvg(Temperature)
			DVal_avg=Dvalue_Time*10.0**((Dvalue_Temp-avg_T)/zvalue)
			LogRed=dt/DVal_avg
			
			TotalLogRed=scr.cumsum(LogRed)
			TotalLogRed.insert(0,0.0) # at time=0 TotalLogRed(1)=0
			
			if(CurTemperatureRangeInfo != None):
				WS[Row, Col] = {'value':CurTemperatureRangeInfo, 'weight':"bold"}
				Row += 1
			
			for i in range(len(Time)):
				WS[Row+i, Col] = Time[i]
				WS[Row+i, Col+1] =Temperature[i]
				WS[Row+i, Col+2] =str(round(LethalRate[i], 3))
				WS[Row+i, Col+3] = str(round(DValue[i], 3))
				WS[Row+i, Col+4] = str(round(TotalLogRed[i], 3))
				WS[Row+i, Col+5] = str(round(FValue[i], 2))
			
			
			return Row + len(Time)  #Current Row, 
		
		
		range_time=gui.Range(self.m_txtTime.GetValue()) 
		range_T = gui.Range(self.m_txtTemperature.GetValue())
		
		#How many temperature locations? Each column should represent a single location
		NTempLocs=range_T.ncols() 
		
		row, col=0,0 #which row shall we print on the grid
		
		Headers=["Time ", "Temperature", "Lethality Rate", "D Value","Total Log Reduction", "F-Value"]
		
		for header in Headers:
			WS[row, col] = {'value': header, 'style':"italic"}
			col+= 1
		
		col=0
		if(NTempLocs>1): 
			row  += 2 
		else: 
			row +=1 
		
		for i in range(NTempLocs):
			status=None
			CurTemperatureRangeInfo=None
			
			if(NTempLocs>1):
				CurTemperatureRangeInfo = str(range_T.subrange(row=0, col=i, nrows=-1, ncols=1))
			
			vtime = scr.Vector([i for i in range_time])
			vtemperature = scr.Vector([i for i in range_T.col(i)]) 
			row = Compute(vtime, vtemperature, row, col, CurTemperatureRangeInfo) 
		
		row += 2
		col = 0
		
		
		event.Skip()



if __name__ == "__main__":
	frm = frmFoodThermalProc(None) 
	frm.Show()

