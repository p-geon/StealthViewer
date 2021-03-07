
"""
def decorate_message(func):
	def wrapper(*args, **kwargs):

		print(" "+"="*30)
		print(f"|{__name__}/{func.__name__}")
		print("|" + "-"*30)
		func(*args, **kwargs)
		print(" "+"="*30)
		print(" ")
	return wrapper
"""
def define_crop(crop_size, H, W, pos):
	# lambdas
	calc_pos_center = lambda height, width: (height//2, width//2)
	calc_top = lambda crop_size: crop_size[0]//2
	calc_bottom = lambda crop_size, height: height-crop_size[0]//2
	calc_left = lambda crop_size: crop_size[1]//2
	calc_right = lambda crop_size, width: width-crop_size[1]//2

	def get_crop_func(crop_size: tuple, center: tuple) -> "crop function":
		return lambda img: img[center[0]-(crop_size[0]//2):center[0]+(crop_size[0]//2),  center[1]-(crop_size[1]//2):center[1]+(crop_size[1]//2)]

	# get center position
	if(pos=="center"):
		cH, cW = calc_pos_center(H, W)
	elif(pos=="top/left"):
		cH, cW = calc_top(crop_size), calc_left(crop_size)
	elif(pos=="top/right"):
		cH, cW = calc_top(crop_size), calc_right(crop_size, W)
	elif(pos=="bottom/left"):
		cH, cW = calc_bottom(crop_size, H), calc_left(crop_size)
	elif(pos=="bottom/right"):
		cH, cW = calc_bottom(crop_size, H), calc_right(crop_size, W)
	else:
		raise ValueError("invalid pos. choice in ['center', 'top/left', 'top/right', 'bottom/left', 'bottom/right']")
	return get_crop_func(crop_size, center=(cH, cW))
