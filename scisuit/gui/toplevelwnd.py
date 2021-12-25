import wx

def FindTopLevelWindow(obj):

	if(isinstance(obj, wx.Window) == False):
		raise TypeError("obj must be of type wx.Window")

	if(obj.IsTopLevel()):
		return obj

	TopLevelWindow = obj.GetParent()

	Depth = 1
	MAXDEPTH = 10
	while(TopLevelWindow.IsTopLevel() == False and Depth<=MAXDEPTH):
		TopLevelWindow = TopLevelWindow.GetParent()
		Depth += 1
	
	#this to happen is highly unlikely
	if(Depth> MAXDEPTH):
		raise RuntimeError("Could not find a top level window")
	
	return TopLevelWindow