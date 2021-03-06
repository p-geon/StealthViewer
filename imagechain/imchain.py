import sys
#from easydict import EasyDict
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageStat, Image
import skimage
from skimage import io
from skimage.transform import resize
from skimage import exposure, img_as_ubyte
from imgcat import imgcat


int16_to_uint16 = lambda img: (img + 65536//2) # [-32,768-32,767] -> [0-65,535]
int16_to_uint8 = lambda img: (int16_to_uint16(img)/255).astype(np.uint8) # [-32,768-32,767] -> [0-255]
uint8_to_float64 = lambda img: img.astype(np.float64)/255.0 # [0-255] -> [0.0f-1.0f]
float_to_uint8 = lambda img: (img*255).astype(np.int) # [0.0f-1.0f] -> [0-255]
norm_minmax = lambda img: (img - np.min(img))/(np.max(img)-np.min(img)) # [min-max] -> [0.0f-1.0f]
norm_zscore = lambda img: (img-np.mean(img))/np.std(img)

# chain
class ImageChain:
	def __init__(self, disp=["plt", "iterm"][1]):
		"""ImageChain core"""
		self.img = None	
		self.fname = "unknown.unknown"
		self.get_img = lambda: self.img
		self.disp = disp

		self.__get_height = lambda: self.img.shape[0]
		self.__get_width = lambda: self.img.shape[1]
		self.__get_dtype_1px = lambda: type(self.img.flatten()[0])

	def load(self, path: str):
		"""ImageChain <- load(path)"""
		img = io.imread(path) # uint8
		self.img = uint8_to_float64(img)
		self.fname = path.split("/")[-1]
		return self

	def set_img(self, img):
		"""ImageChain <- Image"""
		self.img = img
		return self

	def show_fname(self, endl=None):
		"""show original filename (not dir)"""
		print(f"filename: {self.fname}")
		if(endl!=None): print(endl)
		return self

	def crop(self, crop_size: "(height, width)", pos=['center', 'top/left', 'top/right', 'bottom/left', 'bottom/right'][0]) -> None:
		"""img -> crop(img)"""
		H, W = self.__get_height(), self.__get_width()

		# lambdas
		calc_pos_center = lambda height, width: (height//2, width//2)
		calc_top = lambda crop_size: crop_size[0]//2
		calc_bottom = lambda crop_size, height: height-crop_size[0]//2
		calc_left = lambda crop_size: crop_size[1]//2
		calc_right = lambda crop_size, width: width-crop_size[1]//2
		cropping = lambda img, crop_size, center: img[center[0]-(crop_size[0]//2):center[0]+(crop_size[0]//2),  center[1]-(crop_size[1]//2):center[1]+(crop_size[1]//2)]

		# get center position
		if(pos=="center"):
			cH, cW = calc_pos_center(H, W)
		elif(pos=="top/left"):
			cH, cW = calc_top(crop_size), calc_left(crop_size)
		elif(pos=="top/right"):
			cH, cW = calc_top(crop_size), calc_right(crop_size, W)
		elif(pos=="bottom/left"):
			cH, cW = calc_bottom(crop_size, H), calc_left(crop_size)
		elif(pos=="bottom/right"):
			cH, cW = calc_bottom(crop_size, H), calc_right(crop_size, W)
		else:
			raise ValueError("invalid pos. choice in ['center', 'top/left', 'top/right', 'bottom/left', 'bottom/right']")
		print(cH, cW, crop_size)
		# crop
		self.img = cropping(self.img, crop_size, (cH, cW))
		return self

	def clip(self, value=(0.0, 1.0)) -> "self":
		a_min, a_max = value
		np.clip(self.img, a_min=0.0, a_max=1.0)
		return self

	def scale(self, ratio: float) -> "self":
		self.img = resize(image=self.img
			, output_shape=[int(self.__get_height()*ratio), int(self.__get_width()*ratio)])
		return self

	def half(self) -> "self":
		"""checked"""
		self.scale(ratio=0.5)
		return self

	def quarter(self) -> "self":
		"""checked"""
		self.scale(ratio=0.25)
		return self

	def align(self, width: int) -> "self":
		return self.scale(ratio=width/self.__get_width())

	def astype(self, method) -> "self":
		if(method=="int16_to_uint8"):
			self.img = int16_to_uint8(self.img)
		elif(method=="uint8_to_float64"):
			self.img = uint8_to_float64(self.img)
		elif(method=="float_to_uint8"):
			self.img = float_to_uint8(self.img)
		else:
			raise ValueError("invalid method")
		return self

	def status(self, tabs=1) -> "self":
		_tabs = "\t"*tabs
		img = self.img
		_dtype_full = f'{type(img)}'
		_dtype_1px = f'{self.__get_dtype_1px()}'
		print("="*30 + "\nStatus\n" + "-"*30)
		print("  [Image Statistics]")
		# :と<の間にスペース無いとバグる。<と数字の間にスペースが有ると比較演算になってバグる
		print(f"    max:    {np.max(img):.3f} / min: {np.min(img):.3f}")
		print(f"    mean:   {np.mean(img):.3f} (std: {np.std(img):.3f})")
		print(f"    median: {np.median(img):.3f}")
		print("")
		print(f"  [pixel information]")
		print(f"    shape: {f'{img.shape}'}, num_pixels: {str(self.__get_height()*self.__get_width())}")
		print(f"    dtype: image: {_dtype_full}, px: {_dtype_1px}")
		print("="*30)
		return self

	def memory(self) -> "self":
		_mem = sys.getsizeof(self.img)
		print(f"spent mem: {_mem}[byte]")
		return self

	def show(self, height=4) -> "self":
		if(self.disp == "plt"):
			del height
			plt.figure()
			if(len(self.img.shape)==3):
				plt.imshow(self.img)
			else:
				plt.imshow(self.img, cmap = "gray", vmin=0.0, vmax=1.0)
			plt.show()
			plt.close()
			return self
		elif(self.disp == "iterm"):
			# あくまでもターミナルの表示サイズになる
			if("float" in f"{self.__get_dtype_1px()}"):
				_img = float_to_uint8(self.img)
			else:
				_img = self.img
			imgcat(_img, height=height)
			return self

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
		plt.figure()
		if(dtype=="int16"):
			plt.hist(img_as_ubyte(self.img.flatten()), bins=np.arange(65536+1))
		else:
			plt.hist(img_as_ubyte(exposure.rescale_intensity(self.img)).flatten(), bins=np.arange(256+1))
		plt.show()
		return self

	def add(self, val: float) -> "self":
		self.img += val
		return self

	def mul(self, val: float) -> "self":
		self.img *= val
		return self

	def save(self, path="untitled.png") -> "self":
		io.imsave(path, self.img)
		print(f"saved {path}")
		return self

	def end(self) -> None:
		"""delete image object."""
		del self.img
		return None