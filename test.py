import sys
import unittest

#from imagechain import imagechain
#from scripts.imagechain import ImageChain
from imagechain import ImageChain
from imagechain import ImcFlow
from imagechain import imflow as imf

print(f"python: {sys.version}")



class TestIMGChain(unittest.TestCase):
	"""test imagechain module"""
	def setUp(self):
		self.path_img = "./src/fff.png"
		print('setUp called.')

	@unittest.skip
	def test_calc(self):
		print(">>>test calculation<<<")
		imc = ImageChain().load(self.path_img).show("iterm")
		imc = imc.mul(val=-1.0).add(val=1.0).status().show("iterm")

	def test_imcflow(self):
		print(">>>imc flow<<<")

		img = ImageChain().load(self.path_img).status().show("iterm").get_img()

		img = ImcFlow(flow=[imf.Mul(0.5), imf.Status(), imf.Add(0.5)]).flow(img)

		ImageChain().set_img(img).show("iterm")
		
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