import wx


class Frame(wx.Frame):
      """
           Implements OnClose event to provide a closeable frame

      """
      def __init__( self, 
            parent=None, 
            id=wx.ID_ANY, 
            title=wx.EmptyString, 
            pos=wx.DefaultPosition, 
            size=wx.DefaultSize, 
            style=wx.DEFAULT_FRAME_STYLE, 
            name=wx.FrameNameStr ):

            wx.Frame.__init__ ( self, 
                parent, 
                id = id, 	
                title = title, 
                pos = pos, 
                size = size, 
                style = style,
                name=name )
      
            self.Bind(wx.EVT_CLOSE, self.OnClose)
      

      def OnClose(self, event):
            self.Hide()
            self.Destroy()
            
            event.Skip()