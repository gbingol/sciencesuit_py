from scisuit.stats import quantile

def median(x, Sorted=False):
	retVal = None
	try:
		retVal = quantile(x, 0.5, Sorted)
	except Exception as e:
		print(e)
		raise TypeError(e) from None
	
	return retVal