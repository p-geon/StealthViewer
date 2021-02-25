def check_img(func):
	def wrapper(*args, **kwargs):
		print('--image information-')
		img = args[0]
		print(f"shape: {img.shape}")
		print(f"dtype: {type(img)}")
		print(f"max: {img.max()}")
		print(f"min: {img.min()}")
		print(f"ave: {np.mean(img)}")
		plt.figure()
		plt.hist(img, bins=20)
		plt.show()
		print('------')
		func(*args, **kwargs)
	return wrapper

def main():
	path = "./src/fff.png"
	img = Image.open(path)
	stat = ImageStat.Stat(img)
	print('pixel num:', stat.count) # Number of Pixel
	print('pixel sum:', stat.sum)   # Sum of Pixel Value
	print('pixel mean:', stat.mean) # Mean of Pixel Values
	print('pixel variance:', stat.var) #variance of all Pixels
	print('pixel stddev:', stat.stddev) #standerd deviation
