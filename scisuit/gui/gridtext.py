import wx

import scisuit.gui as gui


def _GetVariable(txt):
     ws = gui.activeworksheet()
     rng = ws.selection()
     txt.SetValue(str(rng))
     txt.GetParent().Raise()


class frmGridSelection (wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self,
                     parent,
                     id=wx.ID_ANY,
                     title=wx.EmptyString,
                     pos=wx.DefaultPosition,
                  size=wx.Size(500, 48),
                     style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		mainSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.m_textCtrl = wx.TextCtrl(
		    self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		mainSizer.Add(self.m_textCtrl, 1, wx.ALL, 5)

		self.m_btnOK = wx.Button(self, wx.ID_ANY, u"OK",
		                         wx.DefaultPosition, wx.DefaultSize, 0)
		mainSizer.Add(self.m_btnOK, 0, wx.ALL, 5)

		self.SetSizerAndFit(mainSizer)
		self.Layout()

		self.Centre(wx.BOTH)

		self.m_btnOK.Bind(wx.EVT_BUTTON, self.btnOK_OnButtonClick)
		self.m_Worksheet = gui.activeworksheet()
		self.m_Worksheet.bind(_GetVariable, self.m_textCtrl)

	def SetOwnerTopLevelWindow(self, wnd):
		self.m_OwnerTopLevelWnd = wnd

	def SetOwnerTextCtrl(self, txtctrl):
		self.m_OwnerTextCtrl = txtctrl

	def btnOK_OnButtonClick(self, event):
		self.m_Worksheet.unbind(_GetVariable)
		self.Hide()
		self.Destroy()
		self.m_OwnerTopLevelWnd.Show()
		self.m_OwnerTextCtrl.SetValue(self.m_textCtrl.GetValue())

		event.Skip()


class GridTextCtrl(wx.TextCtrl):
     def __init__(self,
                   parent,
                   id=wx.ID_ANY,
                   value=wx.EmptyString,
                   pos=wx.DefaultPosition,
                   size=wx.DefaultSize,
                   style=0,
                   validator=wx.DefaultValidator,
                   name=wx.TextCtrlNameStr):

          wx.TextCtrl.__init__(self, parent, id, value, pos,
                               size, style, validator, name)

          self.m_Worksheet = None
          self.m_TopLevelWindow = parent

          self.SetBackgroundColour(wx.Colour(128, 255, 255))

          while(self.m_TopLevelWindow.IsTopLevel() == False):
              self.m_TopLevelWindow = self.m_TopLevelWindow.GetParent()

          self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
      

     def OnLeftDown(self, event):
            frm = frmGridSelection(None)
            frm.SetOwnerTopLevelWindow(self.m_TopLevelWindow)
            frm.SetOwnerTextCtrl(self)
            frm.Show()
            self.m_TopLevelWindow.Hide()
            event.Skip()




            
