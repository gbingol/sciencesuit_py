"""
It is recommended NOT to change or to edit this file

This file is run when the system starts, so anything wrong here will 
either prevent system from starting or will break things
"""


import sys

#access to scisuit package (or any other folder inside installation folder designated as package)
sys.path.append('./')


"""
Following is needed by wxPython

When designing wxPython apps do not use app.MainLoop in your application
since there can only be one main loop in wxPython in a single process. 

Attempting to use app.MainLoop elsewhere will crash the whole system 
unless a subprocess is used.
"""

import pkgutil

wxInstalled = False
for pkg in pkgutil.iter_modules():
	if pkg.name == "wx":
		wxInstalled = True
		break
		
if(wxInstalled):
	import wx
	app=wx.App(useBestVisual=True)
	app.MainLoop() #there can only be one main loop in wxPython
