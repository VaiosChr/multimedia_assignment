import numpy as np
from scipy.fftpack import dct, idct

# Returns the DCT of a block
def blockDCT(block):
    return dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')


# Returns the inverse DCT of a block
def iBlockDCT(block):
    return idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')