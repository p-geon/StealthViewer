import numpy as np
from easydict import EasyDict

from imagechain.type_conversion import tc

class InstantiateImage:
	def __init__(self, shape: list):
		self.generic = None
		self.H = shape[0]
		self.W = shape[1]
	
		if(len(shape)==3):
			self.C = shape[2]
			self.generic = "Color"
		elif(len(shape)==4): # RGBa
			self.C = shape[2]
			self.a = shape[3]
			self.generic = "RGBa"
		elif(len(shape)==2): # GrayScale
			self.generic = "GrayScale"
		else: #???
			raise ValueError("Invalid tensor shape")

		self.dict_generic_shape = {
			"Color": [self.H, self.W, 3]
		  , "RGBa": [self.H, self.W, 4]
		  , "GrayScale": [self.H, self.W]
		}

		self.extrude = lambda func: func(self.dict_generic_shape[self.generic])

	def zeros(self):
		return self.extrude(func=np.zeros)

	def ones(self):
		return self.extrude(func=np.ones)

	def white_uint8(self):
		return tc.float_to_uint8(self.ones())

	def noise_float(self):
		return np.random.rand(self.H, self.W, self.C)

	def noise_uint8(self):
		return tc.float_to_uint8(self.noise_float())

ii = EasyDict({
	  "zeros": lambda shape: InstantiateImage(shape).zeros()
	, "ones": lambda shape: InstantiateImage(shape).ones()
    , "white": {
		  "as_uint8": lambda shape: InstantiateImage(shape).white_uint8()
		, "as_float": lambda shape: InstantiateImage(shape).ones()
	}
	, "noise": {
		  "as_float": lambda shape: InstantiateImage(shape).noise_float()
		, "as_uint8": lambda shape: InstantiateImage(shape).noise_uint8()
	}
	, "square": {
		  "black": lambda: InstantiateImage([256, 256, 3]).zeros()
		, "white": lambda: InstantiateImage([256, 256, 3]).ones()
	}
	})