import os
import sys
from easydict import EasyDict
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageStat, Image
import skimage
from skimage import io
from skimage.transform import resize
from skimage import exposure, img_as_ubyte
from skimage.util.dtype import img_as_float

from imgcat import imgcat

from imagechain.type_conversion import tc
from imagechain.utils import define_crop, decorate_message

# chain
class ImageChain:
	"""
	基本はfloat64。明示したときのみuint8
	"""
	def __init__(self, disp=["plt", "iterm"][1]):
		"""ImageChain core"""
		self.img = None	
		self.fname = "unknown.unknown"
		self.get_img = lambda: self.img
		self.disp = disp
		self.img_hist = [] # list of img

		self.__get_height = lambda: self.img.shape[0]
		self.__get_width = lambda: self.img.shape[1]
		self.__get_dtype_1px = lambda: type(self.img.flatten()[0])
	
	def set_img(self, img):
		"""ImageChain <- Image"""
		self.img = img
		return self
	"""
	<Push/Pop>
	"""
	def push(self):
		self.img_hist.append(self.img)
		return self

	def pop(self):
		self.img = self.img_hist.pop()
		return self

	"""
	<I/O>
	- save
	"""
	def load(self, path: str):
		"""ImageChain <- load(path)"""
		img = io.imread(path) # uint8
		#self.img = tc.uint8_to_float64(img)
		self.img = img_as_float(img)
		self.fname = path.split("/")[-1]
		return self
		
	def save(self, path="untitled.png") -> "self":
		"""save via skimage.io"""
		io.imsave(path, self.img)
		print(f"saved {path}")
		return self

	"""
	<conversion>
	- astype (type conversion)
	- clip
	"""
	def astype(self, method) -> "self":
		self.img = tc[method](self.img)
		return self

	def clip(self, value=(0.0, 1.0)) -> "self":
		a_min, a_max = value
		np.clip(self.img, a_min=0.0, a_max=1.0)
		return self

	"""
	<transform>
	- crop
	"""
	def crop(self, crop_size: "(height, width)", pos=['center', 'top/left', 'top/right', 'bottom/left', 'bottom/right'][0]) -> None:
		"""img -> crop(img)"""
		self.img = define_crop(crop_size
					, H=self.__get_height(), W=self.__get_width()
					, pos=pos)(self.img)
		return self

	def scale(self, ratio: "shrink/expand ratio, tuple(W, H)") -> "self":
		self.img = resize(image=self.img
			, output_shape=[int(ratio[0]*self.__get_height()), int(ratio[1]*self.__get_width())]
			)
		return self

	def align(self, width: int) -> "self":
		_r = width/self.__get_width()
		return self.scale(ratio=(_r, _r))

	def pool(self, size=(2, 2)) -> "self":
		self.scale(ratio=(1.0/size[0], 1.0/size[1]))
		return self

	def unpool(self, size=(2, 2)) -> "self":
		self.scale(ratio=size)
		return self

	"""
	<operators>
	- add
	- mul
	"""
	def add(self, val: float) -> "self":
		self.img += val
		return self

	def sub(self, val: float) -> "self":
		self.img -= val
		return self

	def mul(self, val: float) -> "self":
		self.img *= val
		return self

	def div(self, val: float) -> "self":
		self.img /= val
		return self

	"""
	<visualize>
	- show
	- show3d
	- hist
	"""
	def show(self, img_height=4) -> "self":
		if(self.disp=="plt"):
			plt.figure()
			if(len(self.img.shape)==3):
				plt.imshow(self.img)
			else:
				plt.imshow(self.img, cmap = "gray", vmin=0.0, vmax=1.0)
			plt.show()
			plt.close()
			return self
		elif(self.disp=="iterm"):
			self.__show_with_iterm(self.img, type_img=f"{self.__get_dtype_1px()}", img_height=img_height)
			return self
		else:
			raise ValueError("self.disp is invalid. choice in plt/iterm")
		
	def show3d(self) -> "self":
		H, W = np.meshgrid(
			  np.linspace(start=0, stop=self.__get_height(), num=self.__get_height())
			, np.linspace(start=0, stop=self.__get_width(), num=self.__get_width())
			)

		ax = plt.axes(projection='3d')
		ax.plot_surface(H, W, self.img, rstride=1, cstride=1,
						cmap='viridis', edgecolor='none')
		ax.set_title('3D Plotting')
		return self

	def hist(self, dtype="int16") -> "self":
		if(self.disp=="plt"):
			plt.figure()
			if(dtype=="int16"):
				plt.hist(img_as_ubyte(self.img.flatten()), bins=np.arange(65536+1))
			else:
				plt.hist(img_as_ubyte(exposure.rescale_intensity(self.img)).flatten(), bins=np.arange(256+1))
			plt.show()
		elif(self.disp=="iterm"):
			tmp_path = "tmp.png"
			plt.figure()
			plt.hist(img_as_ubyte(exposure.rescale_intensity(self.img)).flatten(), bins=np.arange(256+1))
			plt.savefig(tmp_path)
			plt.close()

			img_hist = io.imread(tmp_path)
			img_hist = img_hist[:, :, 0:3] # RGBa->RGB
			self.__show_with_iterm(img_hist, type_img="uint8", img_height=20)
			os.remove(tmp_path)
		return self

	@staticmethod
	def __show_with_iterm(img, type_img, img_height) -> None:
		"""
		あくまでもターミナルの表示サイズになる
		RGBaは表示不可
		"""
		if("float" in type_img):
			_img = tc.float_to_uint8(img)
		else:
			_img = img
		imgcat(_img, height=img_height)
		return None

	def end(self) -> None:
		"""delete image object."""
		del self.img
		return None
	
	"""
	<log>
	- log
	- __log_fname
	- __log_status
	- __log_memory
	"""
	def log(self, method=None) -> "self":
		if(method==None):
			pass
		elif(method=="fname"):
			self.__log_fname()
		elif(method=="status"):
			self.__log_status()
		elif(method=="memory"):
			self.__log_memory()
		return self

	def typrint(self) -> "self":
		_type = f"{self.__get_dtype_1px()}".split("'")[1]
		print(f'> type: {_type}')
		return self

	@decorate_message
	def __log_fname(self) -> "self":
		"""show original filename (not dir)"""
		print(f"| filename: {self.fname}")
		return self
	
	@decorate_message
	def __log_status(self) -> "self":
		_tabs = "\t"
		img = self.img
		_dtype_full = f'{type(img)}'
		_dtype_1px = f'{self.__get_dtype_1px()}'

		print("|  [Image Statistics]")
		# :と<の間にスペース無いとバグる。<と数字の間にスペースが有ると比較演算になってバグる
		print(f"|    max:    {np.max(img):.3f} / min: {np.min(img):.3f}")
		print(f"|    mean:   {np.mean(img):.3f} (std: {np.std(img):.3f})")
		print(f"|    median: {np.median(img):.3f}")
		print(f"|")
		print(f"|  [pixel information]")
		print(f"|    shape: {f'{img.shape}'}, num_pixels: {str(self.__get_height()*self.__get_width())}")
		print(f"|    dtype: image:")
		print(f"|      {_dtype_full}")
		print(f"|    px:")
		print(f"|      {_dtype_1px}")
		return self
	
	@decorate_message
	def __log_memory(self) -> "self":
		_mem = sys.getsizeof(self.img)/(1024**2)
		print(f"| id: {id(self.img)}")
		print(f"| spent mem: {_mem:.3f}[MB]")
		return self
