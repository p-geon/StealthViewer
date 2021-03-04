from scripts.imagechain import ImageChain

if(__name__ == "__main__"):

	import sys
	print(f"python: {sys.version}")
	img = ImageChain().load(path="./src/fff.png").iterm_show().status().show_fname().get()

	imc = ImageChain().set_img(img).scale(ratio=8).status().show()
	imc = imc.mul(val=-1.0).add(val=1.0)
	imc = imc.show_fname()
	img_ndarray = imc.get()