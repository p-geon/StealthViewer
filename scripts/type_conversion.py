import numpy as np

def int16_to_uint8(img):
    """range: -32,768 ～ 32,767"""
    img  = (img + 65536//2) # int16 -> uint16
    img = (img / 255).astype(np.uint8) # uint16 -> uint8
    return img

def uint8_to_norm(img):
    """range: 0-255 -> 0.0f-1.0f"""
    return img.astype(np.float32)/255

def norm_to_uint8(img):
    """range: 0.0f-1.0f -> 0-255"""
    return (img*255).astype(np.int)