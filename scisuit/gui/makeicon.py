import os
import wx

from scisuit.gui import exepath

def makeicon(path):
	"""
	path: image's relative (relative to ScienceSuit's exepath) or full path 
	
	returns an icon
	"""
	if(isinstance(path, str) == False):
		raise TypeError("path must be of type string")
	
	FullPath = None

	if(os.path.relpath(path)):
		FullPath = exepath() + path
	else:
		FullPath = path
	
	if(os.path.exists(FullPath) == False):
		raise ValueError("Invalid path:" + path)

	icon = wx.Icon()
	image = wx.Image()
	image.LoadFile(FullPath)
	bmp=image.ConvertToBitmap()
	icon.CopyFromBitmap(bmp)

	return icon


