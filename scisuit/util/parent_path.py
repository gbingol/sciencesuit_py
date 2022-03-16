import os

"""
The function name is similar to std::filesystem::path::parent_path (in C++)
"""

def parent_path(Path):
	"""
	Path: A relative or full path
	
	If Path = C:\\a\\b\\c.py
	
	returns C:\\a\\b
	
	"""
	if(isinstance(Path, str) == False):
		raise TypeError("path must be of type string")
	
	PathList = os.path.normpath(Path).split(os.sep)
	PathList.pop() #pop the last entry in the list, (i.e. c.py )
	
	#join the list using the default os separator
	ParentPath = os.sep.join(PathList) + os.sep
	
	return ParentPath