import numpy as np

from imagechain import ImageChain

class ImageOperator:
	def __init__(self, img):
		self.img = img


	def shape(self):
		return self.img.shape

	def get_chain(self):
		return ImageChain().set_img(self.img)