from PIL import Image
import numpy as np
from rgb_to_ycrcb import convert2ycrcb, convert2rgb
from dct import blockDCT
from zig_zag import runLength
from quantization import quantizeJPEG
from huffman import huffEnc, huffDec

quantTable = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                          [12, 12, 14, 19, 26, 58, 60, 55],
                          [14, 13, 16, 24, 40, 57, 69, 56],
                          [14, 17, 22, 29, 51, 87, 80, 62],
                          [18, 22, 37, 56, 68, 109, 103, 77],
                          [24, 35, 55, 64, 81, 104, 113, 92],
                          [49, 64, 78, 87, 103, 121, 120, 101],
                          [72, 92, 95, 98, 112, 100, 103, 99]])


# Open the image
image = Image.open("images/baboon.png")
# image = Image.open("lena_color_512.png")

# Convert the image data to numpy arrays
r, g, b = np.array(image.split())
subimg = (4, 4, 4)

# Convert to YCrCb with 4:2:2 subsampling
y, cr, cb = convert2ycrcb(r, g, b, subimg)

dct_y = blockDCT(y[0:8, 0:8])
print(dct_y)
quant = quantizeJPEG(dct_y, quantTable, 1)
runSymbols = runLength(quant, 35)
print(runSymbols)
huffStream = huffEnc(runSymbols)
print(huffStream)
runSymbols = huffDec(huffStream)
print(runSymbols)



# r_new, g_new, b_new = convert2rgb(y, cr, cb, subimg)

# r_img = Image.fromarray(r_new, 'L')
# g_img = Image.fromarray(g_new, 'L')
# b_img = Image.fromarray(b_new, 'L')

# # Create a new image from the RGB channels
# new_image = Image.merge("RGB", (r_img, g_img, b_img))

# # Save the new image to a folder
# new_image.save("images/new_baboon.png")
# # new_image.save("images/new_lena.png")