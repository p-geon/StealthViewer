import sys
import unittest
import numpy as np

#from imagechain import imagechain
#from scripts.imagechain import ImageChain
from imagechain import ImageChain
from imagechain import ImcFlow
from imagechain import Chains
from imagechain import imflow as imf

from imagechain import ii

print(f"python: {sys.version}")

class TestIMGChain(unittest.TestCase):
	"""test imagechain module"""
	def setUp(self):
		self.path_img = "./src/fff.png"
		print('setUp called.')

	@unittest.skip
	def test_imcflow(self):
		"""checked"""
		print(">>>imc flow<<<")
		img = ImageChain().load(self.path_img).status().show().get_img()
		img = ImcFlow(flow=[imf.Mul(0.5), imf.Status(), imf.Add(0.5)]).flow(img)
		ImageChain().set_img(img).show()

	@unittest.skip
	def test_calc(self):
		"""checked"""
		print(">>>test calculation<<<")
		imc = ImageChain().load(self.path_img).show()
		imc = imc.mul(val=-1.0).add(val=1.0).status().show()
	
	@unittest.skip
	def test_transform(self):
		getimg = lambda: ImageChain(disp="iterm").load(self.path_img)
		getimg().half().half().quarter().show()
		getimg().align(width=300).show()
		getimg().scale(ratio=1.5).show()
		
		for pos in ["center", "top/left", "top/right", "bottom/left", "bottom/right", "unknown"]:
			print("pos:", pos)
			getimg().crop((256, 256), pos=pos).show()
	
	@unittest.skip
	def test_save(self):
		getimg = lambda: ImageChain(disp="iterm").load(self.path_img)
		path = "./output/untitled.png"

		getimg().crop((256, 256)).show().save(path)
		ImageChain(disp="iterm").load(path)

	@unittest.skip
	def test_hist(self):
		getimg = lambda: ImageChain(disp="iterm").load(self.path_img)
		getimg().hist()

	@unittest.skip
	def test_log(self):
		_ = ImageChain(disp="iterm").load(self.path_img).show().log("fname").log("status").log("memory")
		_ = ImageChain(disp="iterm").load(self.path_img).astype("float_to_uint8").show().log("fname").log("status").log("memory")

	@unittest.skip
	def test_transform(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.typrint().show().log("status").typrint()
		imc = imc.crop((256, 256), "center").log("status")
		imc = imc.pool().log("status").show().unpool().show().scale((0.1, 0.2)).show().align(100).show()

	@unittest.skip
	def test_pushpop(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.status().show().push().pool((10,10)).status().show().pop().unpool().show()
	
	@unittest.skip
	def test_hr(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.hr(n=10).show().hr(n=50)

	@unittest.skip
	def test_where(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.where()
		imc.where().hr().where()

	@unittest.skip
	def test_pdb(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.show().pdb().show()

	@unittest.skip
	def test_slicing(self):
		imc = ImageChain(disp="iterm").load(self.path_img).show()
		imc = imc.void(
				"for return or Indents"
				).where()
		imc.lmd(func=lambda img: img[0:500, 0:500]).show()
		imc[0:450, 0:450].show()
		imc[0:450, ::-1].show()

	@unittest.skip
	def test_instantiate_image(self):
		imc = ImageChain(disp="iterm").set_img(ii.ones([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.zeros([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.white.as_uint8([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.white.as_float([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.noise.as_float([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.noise.as_uint8([256, 256, 3])).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.square.black()).show().hr()
		imc = ImageChain(disp="iterm").set_img(ii.square.white()).show().hr()		

	@unittest.skip
	def test_timer(self):
		imc = ImageChain(disp="iterm").timer().load("./src/img-CC0/pexels-snapwire-6992.jpg").timer().show()

	@unittest.skip
	def test_fft(self):
		path = "./src/img-CC0/pexels-snapwire-6992.jpg"
		imc = ImageChain(disp="iterm").load(path).crop((256, 256)).color2gray().show().status().hr(
		  ).timer().fft().timer().push().lmd(lambda x:20 * np.log(np.absolute(x))).status().hr(
		  ).show().pop().timer().ifft().timer().lmd(lambda x:x.real).status().hr(
		  ).show()
	
	@unittest.skip
	def test_font(self):
		path = "./src/img-CC0/pexels-snapwire-6992.jpg"
		imc = ImageChain(disp="iterm").load(path).crop((256, 256)).scale(ratio=(1, 1)).astype("float_to_uint8").status().show_with_type().hr()
		imc = imc.show().hr().hist().hr().show3d()
	"""
	@unittest.skip
	def test_iterm_show(self):
		print("test iterm show")
		img = ImageChain().load(path_img).iterm_show().get_img()

	@unittest.skip
	def test_continuous_chain(self):
		print("test continuous chain")
		img = ImageChain().load(path_img).get_img()
		img = ImageChain().set_img(img).get_img()

	@unittest.skip
	def test_show(self):
		print("test show img")
		imc = ImageChain().load(path_img).show()

	@unittest.skip
	def test_transform(self):
		print("test transform")
		imc = ImageChain().load(path_img)
		imc = imc.crop(crop_size=(128, 128), pos="center")
		imc = imc.show()

	@unittest.skip
	def test_information(self):
		print("test information")
		imc = ImageChain().load(path_img).status()
		imc = imc.show_fname()
		imc = imc.end()
	"""

if(__name__ == "__main__"):
	unittest.main()