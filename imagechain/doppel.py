class Doppel:
	"""
	for 2 images
	* double means <type>. istead "doppel"
	"""
	def __init__(self):
		self.imgs = [None, None]
		self.fnames = [None, None]

		self.get_imgs = lambda: self.imgs[0], self.imgs[1] # unchain
		self.diff = lambda: np.abs(self.imgs[0]-self.imgs[1])

	def load(self, paths: tuple):
		"""ImageChain <- load(path x2)"""
		for i, path in enumerate(paths):
			img = io.imread(path) # uint8
			self.imgs[i] = uint8_to_float64(img)
			self.fnames[i] = path.split("/")[-1]
		return self

	def set_imgs(self, imgs: tuple):
		"""ImageChain <- Image x2"""
		self.img[0], self.img[1] = img
		return self

	def check_shape(self):
		"""check same shape or not"""
		if(self.imgs[0].shape==self.imgs[1].shape):
			print("same shape:", self.imgs[0].shape)
			return self
		else:
			print(f"not same shape \nimg1: {self.imgs[0].shape}, img2: {self.imgs[1].shape}")
			return self

	def mae(self):
		""" diff = |img1-img2| """
		mae = self.diff(self.imgs[0], self.imgs[1]).sum()
		print(f"mae: {mae}")
		return self

	def mse(self)
		""" mse = np.sum(||)"""
		mse = (self.diff(self.imgs[0], self.imgs[1])**2).sum()
		print(f"MSE: {mse}")
		return self

	def show_diff(self):
		img_diff = np.abs(img1 - img2)
		# show
		return self

	def psnr(self):
		"""check PSNR"""
		return self

	def ssim(self):
		return self

	def swd(self):
		"""sliced wasserstein distance"""
		return self