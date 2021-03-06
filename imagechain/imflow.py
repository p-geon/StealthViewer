# flow
class Add:
	def __init__(self, val: float):
		self.val = val

	def __call__(self, img):
		return img + self.val

class Mul:
	def __init__(self, val: float):
		self.val = val

	def __call__(self, img):
		return img * self.val

class Status:
	def __init__(self):
		pass

	def __call__(self, img):
		print(img)
		return img

class ImcFlow:
	def __init__(self, flow: "list(class)"):
		self.list_flow = flow
	
	def flow(self, img):
		for f in self.list_flow:
			img = f(img)
		return img
