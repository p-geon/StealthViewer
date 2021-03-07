import os
import sys
import pdb
import time
import inspect
import numpy as np
import matplotlib.pyplot as plt
from imgcat import imgcat
import PIL
from PIL import ImageDraw, ImageFont
import skimage
from skimage import io
from skimage.transform import resize
from skimage import exposure, img_as_ubyte
from skimage.util.dtype import img_as_float
#from scipy.fftpack import fft, ifft

from imagechain.type_conversion import tc
from imagechain.utils import define_crop #, decorate_message

# chain
class ImageChain:
	"""
	基本はfloat64。明示したときのみuint8

	- Core
	- Push/Pop
	- I/O
	- conversion
	- transform
	- operators
	- visualize
	- log
	- debug
	- extra method
	"""
	def __init__(self, disp=["plt", "iterm"][1]):
		"""ImageChain core"""
		self.img = None	
		self.fname = "unknown.unknown"
		self.disp = disp
		self.img_hist = [] # list of img
		self.time = None
		self.__tmp_path = "tmp.png"

		# method
		self.get_img = lambda: self.img
		self.__get_height = lambda: self.img.shape[0]
		self.__get_width = lambda: self.img.shape[1]
		self.__get_dtype_1px = lambda: f"{type(self.img.flatten()[0])}".split("'")[1]

	def set_img(self, img):
		"""ImageChain <- Image"""
		self.img = img
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
	<Push/Pop>
	"""
	def push(self):
		self.img_hist.append(self.img)
		return self

	def pop(self):
		self.img = self.img_hist.pop()
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

	def gray2color(self) -> "self":
		gs = self.img
		self.img = np.tile(self.img[np.newaxis], (1, 1, 3))
		return self

	def color2gray(self) -> "self":
		self.img = np.mean(self.img, axis=2)
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

	def fft(self) -> "self":
		#self.img = fft(self.img)
		self.img = np.fft.fftshift(np.fft.fft2(self.img))
		return self

	def ifft(self) -> "self":
		#self.img = ifft(self.img)
		self.img = np.fft.ifft2(np.fft.fftshift(self.img))
		return self

	def __invert__(self) -> "self":
		_type = self.__get_dtype_1px()

		if("float" in _type):  # float32/64
			self.img = 1 - self.img
			return self
		elif("uint8" in _type):
			self.img = 255 - self.img
			return self
		else:
			raise ValueError("use float or uint8")
			
	"""
	<visualize>
	- show
	- show3d
	- hist
	"""
	def show(self, img_height=None) -> "self":
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
			self.__error_disp_invalid()
		
	def show3d(self) -> "self":
		H, W = np.meshgrid(
			  np.linspace(start=0, stop=self.__get_height(), num=self.__get_height())
			, np.linspace(start=0, stop=self.__get_width(), num=self.__get_width())
			)

		if(self.disp=="plt"):
			"""TBD"""
			pass
		elif(self.disp=="iterm"):
			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1)
			ax = plt.axes(projection='3d')
			ax.plot_surface(H, W, np.mean(self.img, axis=2), rstride=1, cstride=1,
				cmap='viridis', edgecolor='none')
			ax.set_title('3D Plotting')
			plt.savefig(self.__tmp_path)

			self._read_and_remove_tmpfile()
		else:
			self.__error_disp_invalid()
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
			plt.figure()
			plt.hist(img_as_ubyte(exposure.rescale_intensity(self.img)).flatten(), bins=np.arange(256+1))
			plt.savefig(self.__tmp_path)
			plt.close()
			self._read_and_remove_tmpfile()
		else:
			self.__error_disp_invalid()
		return self

	def _read_and_remove_tmpfile(self) -> None:
		_img = io.imread(self.__tmp_path)
		_img = _img[:, :, 0:3] # RGBa->RGB
		self.__show_with_iterm(_img, type_img="uint8", img_height=16)
		os.remove(self.__tmp_path)
		return None

	def show_with_type(self) -> "self":

		_type = self.__get_dtype_1px()
		_height = self.__get_height()

		_font_size = _height//10
		_rect_range = (2, 2, 2+int(_font_size*7), 2+int(_font_size*1.6))
		_pos_text = (8, 4) # offset: (left, top)
		_font = ImageFont.truetype("src/fonts-CC0/Route159-Regular.otf", _font_size)

		img_pil  = PIL.Image.fromarray(self.img)
		pil_draw = PIL.ImageDraw.Draw(img_pil)
		# 順序がおかしいので注意: (x1, y1, x2, y2)
		pil_draw.rectangle(_rect_range, fill=(0, 0, 0), outline=(255, 255, 255))
		pil_draw.text(_pos_text, _type, font=_font)
		img = np.array(img_pil)

		self.__show_with_iterm(img, type_img=_type)
		return self

	@staticmethod
	def __show_with_iterm(img, type_img, img_height=None) -> None:
		"""
		あくまでもターミナルの表示サイズが基準
		RGBaは表示不可
		"""
		if("float" in type_img):
			_img = tc.float_to_uint8(img)
		else:
			_img = img

		if(img_height==None):
			img_height = int(0.030*img.shape[0])+1
		imgcat(_img, height=img_height)
		return None

	@staticmethod
	def __error_disp_invalid() -> "raise":
		raise ValueError("self.disp is invalid. choice in plt/iterm")


	"""
	<log>
	- status
	- typrint
	- hr
	"""
	def status(self) -> "self":
		_tabs = "\t"
		img = self.img
		_dtype_full = f'{type(img)}'
		_dtype_1px = self.__get_dtype_1px()
		_mem = sys.getsizeof(self.img)/(1024**2)
		_frame = inspect.currentframe().f_back

		print(" "+"="*30)
		print(f"| <<<Status>>>")
		print(f"|" + "-"*30)
		print(f"| original filename: {self.fname}")
		print(f"|")
		print(f"|  [Image Statistics]")
		# :と<の間にスペース無いとバグる。<と数字の間にスペースが有ると比較演算になってバグる
		print(f"|    max:    {np.max(img):.3f} / min: {np.min(img):.3f}")
		print(f"|    mean:   {np.mean(img):.3f} (std: {np.std(img):.3f})")
		print(f"|    median: {np.median(img):.3f}")
		print(f"|")
		print(f"|  [pixel information]")
		print(f"|    shape: {f'{img.shape}'}")
		print(f"|    num_pixels: {self.__get_height()*self.__get_width():,}[px]")
		print(f"|    dtype(image)")
		print(f"|      {_dtype_full}")
		print(f"|    dtype(pixel)")
		print(f"|      {_dtype_1px}")
		print(f"|")
		print(f"|  [performance]")
		print(f"|    spent mem: {_mem:.3f}[MB]")
		print(f"|    id: {id(self.img)}")
		print(f"|")
		print(f"|  [code position]")
		print(f"|    script: {os.path.basename(_frame.f_code.co_filename)}")
		print(f"|    func: {_frame.f_code.co_name}")
		print(f"|    line: {_frame.f_lineno}")
		print(" "+"="*30)
		print(" ")
		return self

	def typrint(self) -> "self":
		_type = f"{self.__get_dtype_1px()}".split("'")[1]
		print(f'> type: {_type}')
		return self

	def hr(self, n=30) -> "self":
		print("-"*n)
		return self

	"""
	<debug>
	- pdb
	- void (?) 不要？
	- lmd
	"""
	def pdb(self) -> "self":
		pdb.set_trace()
		return self

	def void(self, memo="you can write free memo.") -> "self":
		return self

	def lmd(self, func) -> "self": # lambda
		self.img = func(self.img)
		return self

	def timer(self) -> "self":
		if(self.time==None):
			print("> initialize timer")
		else:
			_spent_time = time.time() - self.time
			print(f"> spent time: {_spent_time:.5f}")
		self.time = time.time()
		return self

	"""
	<extra method>
	- __call__
	- __getitem__
	"""
	
	def __call__(self) -> "image":
		return self.img

	def __getitem__(self, val: slice) -> "self":
		print(val)
		H = val[0]
		W = val[1]
		H1, H2, H3 = H.start, H.stop, H.step
		W1, W2, W3 = W.start, W.stop, W.step
		self.img = self.img[H1:H2:H3, W1:W2:W3]#, C1:C2]
		return self