import tifffile

def load_img(fname):
	if(fname in ".tif"):
		img = tifffile.imread(fname)
	else:
		img = io.imread(fname)
	return img