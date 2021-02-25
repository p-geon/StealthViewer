import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageStat, Image

import skimage
from skimage import io
from skimage.transform import resize

from imgcat import imgcat

class ImageChain:
	"""
	ImgObj:
		crop
		clip
		norm
		scale
		align
		show
		iterm_show: show a image for iterm2
		hist
		get
	"""
	def __init__(self, path: str):
		self.img = io.imread(path)

	def crop(self, crop_size: "(height, width)", pos=["center", "left-top", "right-top", "left-bottom", "right-bottom"][0]) -> None:
		"""
		<center>:
			□□□□
			□■□□ => ■□
			□□■□ => □■
			□□□□
		"""
		_height = self.img.shape[0]
		_width  = self.img.shape[1]

		if(pos=="center"):
			crop_pos = (_height//2, _width//2)
		elif(pos=="left-top" or pos=="right-top" or pos=="left-bottom" or "right-bottom"):
			pass
		else:
			raise ValueError("invalid pos")

		self.img = self.img[crop_pos[0]-crop_size[0]//2:crop_pos[0]+crop_size[0]//2, crop_pos[1]-crop_size[1]//2:crop_pos[1]+crop_size[1]//2]
		return self

	def clip(self, value=(0.0, 1.0)) -> None:
		a_min, a_max = value
		np.clip(self.img, a_min=0.0, a_max=1.0)
		return self

	def norm(self, method="0to255->0to1") -> None:
		if(method=="0to255->0to1"):
			self.img = self.img.astype(np.float32)/255.0
		elif(method=="0to255->-1to1"):
			pass
		elif(method=="0to1->0to255"):
			pass
		else:
			raise ValueError("invalid method")
		return self

	def scale(self, ratio: int) -> None:
		shape_y, shape_x = self.img.shape[0], self.img.shape[1]
		_shape_y, _shape_x = shape_y//ratio, shape_x//ratio
		self.img = resize(image=self.img, output_shape=[shape_y, shape_x])
		return self

	def align(self, width: int) -> None:
		shape_y, shape_x = self.img.shape[0], self.img.shape[1]
		ratio = shape_x/width # float
		_shape_y, _shape_x = shape_y//ratio, shape_x//ratio
		self.img = resize(image=self.img, output_shape=[shape_y, shape_x])
		return self

	def show(self) -> None:
		plt.figure()
		if(len(self.img.shape)==3):
			plt.imshow(self.img)
		else:
			plt.imshow(self.img, cmap = "gray", vmin=0.0, vmax=1.0)
		plt.show()
		plt.close()
		return self

	def iterm_show(self):
		im = skimage.data.chelsea()   # [300, 451, 3] ndarray, dtype=uint8
		imgcat(self.img, height=7)
		return self

	def hist(self) -> None:
		plt.figure()
		plt.hist(self.img, bins=20)
		plt.show()
		return self

	def get(self) -> "image":
		return self.img

if(__name__ == "__main__"):
	img = ImageChain(path="./src/fff.png").iterm_show().get()