import wx

import scisuit.gui as gui


def _GetVariable(txt):
    ws = gui.activeworksheet()
    rng = ws.selection()
    txt.SetValue(str(rng))


class _frmGridSelection (wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, size=wx.DefaultSize, style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP )

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		mainSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.m_textCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		mainSizer.Add( self.m_textCtrl, 3, wx.ALL, 5 )

		self.m_btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
		mainSizer.Add( self.m_btnOK, 1, wx.ALL, 5 )

		self.SetSizerAndFit(mainSizer)
		self.Layout()

		self.m_btnOK.Bind(wx.EVT_BUTTON, self.btnOK_OnButtonClick)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.m_Worksheet = gui.activeworksheet()
		self.m_Worksheet.bind(_GetVariable, self.m_textCtrl)


	def OnClose(self, event): 
		self.m_Worksheet.unbind(_GetVariable)
		self.Hide()
		self.Destroy()
		self.m_OwnerTopLevelWnd.Show()
		event.Skip()


	def SetOwnerTopLevelWindow(self, wnd):
		self.m_OwnerTopLevelWnd = wnd


	def SetOwnerTextCtrl(self, txtctrl):
		if(txtctrl.GetValue() != wx.EmptyString):
			self.m_textCtrl.SetValue(txtctrl.GetValue())
			
		self.m_OwnerTextCtrl = txtctrl



	def btnOK_OnButtonClick(self, event):
		self.m_Worksheet.unbind(_GetVariable)
		self.Hide()
		self.Destroy()
		self.m_OwnerTopLevelWnd.Show()
		self.m_OwnerTextCtrl.SetValue(self.m_textCtrl.GetValue())

		event.Skip()





class GridTextCtrl(wx.TextCtrl):
	def __init__(self, parent):
		wx.TextCtrl.__init__(self, parent)

		self.m_Worksheet = None
		self.m_TopLevelWindow = parent

		self.SetBackgroundColour(wx.Colour(128, 255, 255))

		while(self.m_TopLevelWindow.IsTopLevel() == False):
			self.m_TopLevelWindow = self.m_TopLevelWindow.GetParent()

		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
      

	def OnLeftDown(self, event): 
		frm = _frmGridSelection(None)
		frm.SetTitle(self.m_TopLevelWindow .GetTitle())
		frm.SetOwnerTopLevelWindow(self.m_TopLevelWindow)
		frm.SetOwnerTextCtrl(self)
		frm.Show()
		self.m_TopLevelWindow.Hide()
		event.Skip()




            
