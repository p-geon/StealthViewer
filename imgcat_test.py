from imgcat import imgcat
import skimage
from PIL import Image
import matplotlib.pyplot as plt

# from the content of image (e.g. buffer in python3, str in python2)
imgcat(open("./fff.png"))

# or numpy arrays!
im = skimage.data.chelsea()   # [300, 451, 3] ndarray, dtype=uint8
imgcat(im, height=7)

# matplotlib, PIL.Image, etc.
imgcat(Image.fromarray(im))

fig, ax = plt.subplots(); ax.plot([1, 2, 3, 4, 5])
imgcat(fig)