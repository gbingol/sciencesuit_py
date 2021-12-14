from .material import Material


class ComputedMaterial(Material):
	"""
	Base class for all materials whose properties are computed
	"""
	def __init__(self) -> None: 
	      super().__init__()  