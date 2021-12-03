"""
It is recommended that you do NOT change or edit this file

This file is run when the system starts, so anything wrong here will 
either prevent system from starting or will break things
"""


import sys
import wx

#access to scisuit package (or any other folder inside installation folder designated as package)
sys.path.append('./')


"""
Following is needed by wxPython

When designing wxPython apps do not use app.MainLoop in your application
since there can only be one main loop in wxPython in a single process. 

Attempting to use app.MainLoop elsewhere will crash the whole system 
unless a subprocess is used.
"""
app=wx.App()
app.MainLoop() #there can only be one main loop in wxPython
