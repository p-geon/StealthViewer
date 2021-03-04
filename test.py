from scripts.imagechain import ImageChain

if(__name__ == "__main__"):
	import sys
	print(f"python: {sys.version}")
	img = ImageChain().load(path="./src/fff.png").iterm_show().status().get()
	img = ImageChain().set_img(img).scale(ratio=8).status().show().get()