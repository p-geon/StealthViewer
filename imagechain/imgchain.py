import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageStat, Image

import skimage
from skimage import io
from skimage.transform import resize
from skimage import exposure, img_as_ubyte

from imgcat import imgcat

#import matplotlib
#matplotlib.use('agg')

class ImageChain:
	"""
	ImgObj:
		(transform)
		crop: crop a image
		clip: clip(truncate) value
		norm: TBD
		norm_zscore: TBD
		scale: scale(shrink) a image
		align: scale a image (to decided width)
		(print)
		status: print status
		show: show image by matplot
		show3d: image value as height by matplot
		iterm_show: show a image through iterm2
		hist: show image histgram
		(handle)
		get: return self.img
		end: delete self.img
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
		H, W = self.__get_height(), self.__get_width()
		cH, cW = crop_size

		if(pos=="center"):
			pH, pW = self.__get_center()
		elif(pos=="left-top" or pos=="right-top" or pos=="left-bottom" or "right-bottom"):
			pass
		else:
			raise ValueError("invalid pos")

		self.img = self.img[pH-(cH//2):pH+(cH//2),  pW-(cW//2):pW+(cW//2)]
		return self

	def clip(self, value=(0.0, 1.0)) -> None:
		a_min, a_max = value
		np.clip(self.img, a_min=0.0, a_max=1.0)
		return self

	def norm(self, method="0to255->0to1") -> None:
		"""
		TBD
		val: type:
			0~255: uint8
			0~65535: uint16?
			-32768~32767: int16
			0~1: float32/64 (normalized)
			-1~1: float32/64 (normalized)
		"""
		if(method=="0to255->0to1"):
			self.img = self.img.astype(np.float32)/255.0
		elif(method=="0to255->-1to1"):
			pass
		elif(method=="0to1->0to255"):
			pass
		else:
			raise ValueError("invalid method")
		return self

	def norm_zscore(self) -> None:
		"""TBD"""
		return self

	def scale(self, ratio: int) -> None:
		self.img = resize(image=self.img, output_shape=[self.__get_height()//ratio, self.__get_width()//ratio])
		return self

	def align(self, width: int) -> None:
		return self.scale(ratio=W/width)

	def status(self) -> None:
		print("<<Image Statistics>>")
		img = self.img
		print(f"max\t| {np.max(img):.4f}")
		print(f"min\t| {np.min(img):.4f}")
		print(f"mean\t| {np.mean(img):.4f}")
		print(f"std\t| {np.std(img):.4f}")
		print(f"median\t| {np.std(img):.4f}")
		print("---")
		print(f"<<pixel information>>")
		print(f"shape\t| {img.shape}")
		print(f"num_pixels\t| {self.__get_height()*self.__get_width()}")
		print(f"dtype\t| {type(img)}")
		print(f"dtype (one-pixel)\t| {type(img.flatten()[0])}")

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

	def show3d(self) -> None:
		H, W = np.meshgrid(
			  np.linspace(start=0, stop=self.__get_height(), num=self.__get_height())
			, np.linspace(start=0, stop=self.__get_width(), num=self.__get_width())
			)

		ax = plt.axes(projection='3d')
		ax.plot_surface(H, H, self.img, rstride=1, cstride=1,
						cmap='viridis', edgecolor='none')
		ax.set_title('3D Plotting')
		return self

	def iterm_show(self):
		im = skimage.data.chelsea()   # [300, 451, 3] ndarray, dtype=uint8
		imgcat(self.img, height=7)
		return self

	def hist(self) -> None:
		plt.figure()
		plt.hist(img_as_ubyte(exposure.rescale_intensity(self.img)).flatten(), bins=np.arange(256+1))
		plt.show()
		return self

	def get(self) -> "image":
		return self.img

	def end(self):
		del self.img
		return None

	def __get_width(self) -> int:
		return self.img.shape[1]

	def __get_height(self) -> int:
		return self.img.shape[0]

	def __get_center(self) -> "tuple(height, width)":
		return (self.__get_height(), self.__get_width())

if(__name__ == "__main__"):
	img = ImageChain(path="./src/fff.png").iterm_show().status().hist().end()