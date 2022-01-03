import wx

import scisuit.gui as gui



def _GetVariable(txt):
	ws = gui.activeworksheet()
	rng = ws.selection()
	txt.SetValue(str(rng))


def OnPageChanged(self):
	self.m_Worksheet.unbind("selecting", _GetVariable)
		
	self.m_Worksheet = gui.activeworksheet()
	self.m_Worksheet.bind("selecting", _GetVariable, self.m_textCtrl)


class _frmGridSelection (wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP )

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.m_textCtrl = wx.TextCtrl(self)
		mainSizer.Add( self.m_textCtrl, 3, wx.ALL, 5 )

		self.m_btnOK = wx.Button(self, wx.ID_ANY, u"OK")
		mainSizer.Add( self.m_btnOK, 1, wx.ALL, 5 )

		self.SetSizerAndFit(mainSizer)
		self.Layout()

		self.m_btnOK.Bind(wx.EVT_BUTTON, self.btnOK_OnButtonClick)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.m_Worksheet = gui.activeworksheet()
		self.m_Worksheet.bind("selecting", _GetVariable, self.m_textCtrl)

		self.m_Workbook = gui.Workbook()
		self.m_Workbook.bind("pagechanged", OnPageChanged, self)
	

	
	

	def close(self):
		self.m_Worksheet.unbind("selecting", _GetVariable)
		self.m_Workbook.unbind("pagechanged", OnPageChanged)
		self.Hide()
		self.Destroy()
		self.m_OwnerTopLevelWnd.Show()


	def OnClose(self, event): 
		self.close()
		event.Skip()


	def SetOwnerTopLevelWindow(self, wnd):
		self.m_OwnerTopLevelWnd = wnd


	def SetOwnerTextCtrl(self, txtctrl):
		if(txtctrl.GetValue() != wx.EmptyString):
			self.m_textCtrl.SetValue(txtctrl.GetValue())
			
		self.m_OwnerTextCtrl = txtctrl



	def btnOK_OnButtonClick(self, event):
		self.close()
		self.m_OwnerTextCtrl.SetValue(self.m_textCtrl.GetValue())

		event.Skip()





class GridTextCtrl(wx.TextCtrl):
	def __init__(self, parent):
		wx.TextCtrl.__init__(self, parent)

		self.m_Worksheet = None
		self.m_TopLevelWindow = gui.FindTopLevelWindow(self)

		self.SetBackgroundColour(wx.Colour(128, 255, 255))

		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)


	def OnLeftDown(self, event): 
		frm = _frmGridSelection(None)
		frm.SetTitle(self.m_TopLevelWindow .GetTitle())
		frm.SetOwnerTopLevelWindow(self.m_TopLevelWindow)
		
		icon = wx.Icon(self.m_TopLevelWindow.GetIcon())
		if(icon.IsOk()):
			frm.SetIcon(icon)
			
		frm.SetOwnerTextCtrl(self)
		frm.Show()

		self.m_TopLevelWindow.Hide()
		event.Skip()