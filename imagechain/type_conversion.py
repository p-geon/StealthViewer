import numpy as np
from easydict import EasyDict

int16_to_uint16 = lambda img: (img + 65536//2) # [-32,768-32,767] -> [0-65,535]
int16_to_uint8 = lambda img: (int16_to_uint16(img)/255).astype(np.uint8) # [-32,768-32,767] -> [0-255]

uint8_to_float64 = lambda img: img.astype(np.float64)/255.0 # [0-255] -> [0.0f-1.0f]
float_to_uint8 = lambda img: (img*255).astype(np.int) # [0.0f-1.0f] -> [0-255]

norm_minmax = lambda img: (img - np.min(img))/(np.max(img)-np.min(img)) # [min-max] -> [0.0f-1.0f]
norm_zscore = lambda img: (img-np.mean(img))/np.std(img)

tc = EasyDict({
	  "int16_to_uint16": int16_to_uint16
	, "int16_to_uint8": int16_to_uint8
	, "uint8_to_float64": uint8_to_float64
	, "float_to_uint8": float_to_uint8
	, "norm_minmax": norm_minmax
	, "norm_zscore": norm_zscore
})