import numpy as np
from scipy.fftpack import dct, idct

def blockDCT(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def iBlockDCT(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Generate a random 8x8 integer matrix with values in [0, 255]
random_matrix = np.random.randint(0, 256, size=(8, 8))