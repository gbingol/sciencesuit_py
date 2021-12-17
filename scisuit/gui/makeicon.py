import wx

def makeicon(path):
      """
      given an image full path, returns an icon
      """
      if(isinstance(path, str) == False):
            raise TypeError("path must be of type string")
      
      icon = wx.Icon()
      image = wx.Image()
      image.LoadFile(path)
      bmp=image.ConvertToBitmap()
      icon.CopyFromBitmap(bmp)
      
      return icon


