from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
import numpy as np
from transformations.dct import blockDCT, iBlockDCT
from transformations.quantization import quantizeJPEG, dequantizeJPEG

######### QUESTION 1 #########

# Read image
# img1 = Image.open("images/baboon.png")
# r1, g1, b1 = np.array(img1.split())
# img2 = Image.open("images/lena_color_512.png")
# r2, g2, b2 = np.array(img2.split())

# subimg1 = (4, 2, 2)
# subimg2 = (4, 4, 4)

# # Convert to YCrCb
# y1, cr1, cb1 = convert2ycrcb(r1, g1, b1, subimg1)
# y2, cr2, cb2 = convert2ycrcb(r2, g2, b2, subimg2)

# # Convert back to RGB
# r1_new, g1_new, b1_new = convert2rgb(y1, cr1, cb1, subimg1)
# r2_new, g2_new, b2_new = convert2rgb(y2, cr2, cb2, subimg2)

# r1_new_img = Image.fromarray(r1_new, 'L')
# g1_new_img = Image.fromarray(g1_new, 'L')
# b1_new_img = Image.fromarray(b1_new, 'L')

# r2_new_img = Image.fromarray(r2_new, 'L')
# g2_new_img = Image.fromarray(g2_new, 'L')
# b2_new_img = Image.fromarray(b2_new, 'L')

# # Create a new image from the RGB channels
# new_image1 = Image.merge("RGB", (r1_new_img, g1_new_img, b1_new_img))
# new_image2 = Image.merge("RGB", (r2_new_img, g2_new_img, b2_new_img))

# # Show the images
# new_image1.show()
# new_image2.show()


######### QUESTION 2 #########

qTable = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                          [12, 12, 14, 19, 26, 58, 60, 55],
                          [14, 13, 16, 24, 40, 57, 69, 56],
                          [14, 17, 22, 29, 51, 87, 80, 62],
                          [18, 22, 37, 56, 68, 109, 103, 77],
                          [24, 35, 55, 64, 81, 104, 113, 92],
                          [49, 64, 78, 87, 103, 121, 120, 101],
                          [72, 92, 95, 98, 112, 100, 103, 99]])

# Read image
img1 = Image.open("images/baboon.png")
r1, g1, b1 = np.array(img1.split())
img2 = Image.open("images/lena_color_512.png")
r2, g2, b2 = np.array(img2.split())

subimg1 = (4, 2, 2)
subimg2 = (4, 4, 4)

# Convert to YCrCb
y1, cr1, cb1 = convert2ycrcb(r1, g1, b1, subimg1)
y2, cr2, cb2 = convert2ycrcb(r2, g2, b2, subimg2)

y1_dct = np.zeros(y1.shape)
cr1_dct = np.zeros(cr1.shape)
cb1_dct = np.zeros(cb1.shape)

y2_dct = np.zeros(y2.shape)
cr2_dct = np.zeros(cr2.shape)
cb2_dct = np.zeros(cb2.shape)

# Break the components in 8x8 blocks

# For luminance components
for i in range(0, y1.shape[0], 8):
    for j in range(0, y1.shape[1], 8):
        y1_dct[i:i+8, j:j+8] = blockDCT(y1[i:i+8, j:j+8])
        y2_dct[i:i+8, j:j+8] = blockDCT(y2[i:i+8, j:j+8])

        # Quantize the coefficients
        y1_dct[i:i+8, j:j+8] = quantizeJPEG(y1_dct[i:i+8, j:j+8], qTable, 0.6)
        y2_dct[i:i+8, j:j+8] = quantizeJPEG(y2_dct[i:i+8, j:j+8], qTable, 5)

        # Dequantize the coefficients
        y1_dct[i:i+8, j:j+8] = dequantizeJPEG(y1_dct[i:i+8, j:j+8], qTable, 0.6)
        y2_dct[i:i+8, j:j+8] = dequantizeJPEG(y2_dct[i:i+8, j:j+8], qTable, 5)

        # Calculate inverse DCT
        y1_dct[i:i+8, j:j+8] = iBlockDCT(y1_dct[i:i+8, j:j+8])
        y2_dct[i:i+8, j:j+8] = iBlockDCT(y2_dct[i:i+8, j:j+8])

# For chrominance components
for i in range(0, cr1.shape[0], 8):
    for j in range(0, cr1.shape[1], 8):
        # Calculate DCT
        cr1_dct[i:i+8, j:j+8] = blockDCT(cr1[i:i+8, j:j+8])
        cb1_dct[i:i+8, j:j+8] = blockDCT(cb1[i:i+8, j:j+8])

        # Quantize the coefficients
        cr1_dct[i:i+8, j:j+8] = quantizeJPEG(cr1_dct[i:i+8, j:j+8], qTable, 0.6)
        cb1_dct[i:i+8, j:j+8] = quantizeJPEG(cb1_dct[i:i+8, j:j+8], qTable, 0.6)

        # Dequantize the coefficients
        cr1_dct[i:i+8, j:j+8] = dequantizeJPEG(cr1_dct[i:i+8, j:j+8], qTable, 0.6)
        cb1_dct[i:i+8, j:j+8] = dequantizeJPEG(cb1_dct[i:i+8, j:j+8], qTable, 0.6)

        # Calculate inverse DCT
        cr1_dct[i:i+8, j:j+8] = iBlockDCT(cr1_dct[i:i+8, j:j+8])
        cb1_dct[i:i+8, j:j+8] = iBlockDCT(cb1_dct[i:i+8, j:j+8])

for i in range(0, cr2.shape[0], 8):
    for j in range(0, cr2.shape[1], 8):
        # Calculate DCT
        cr2_dct[i:i+8, j:j+8] = blockDCT(cr2[i:i+8, j:j+8])
        cb2_dct[i:i+8, j:j+8] = blockDCT(cb2[i:i+8, j:j+8])

        # Quantize the coefficients
        cr2_dct[i:i+8, j:j+8] = quantizeJPEG(cr2_dct[i:i+8, j:j+8], qTable, 5)
        cb2_dct[i:i+8, j:j+8] = quantizeJPEG(cb2_dct[i:i+8, j:j+8], qTable, 5)

        # Dequantize the coefficients
        cr2_dct[i:i+8, j:j+8] = dequantizeJPEG(cr2_dct[i:i+8, j:j+8], qTable, 5)
        cb2_dct[i:i+8, j:j+8] = dequantizeJPEG(cb2_dct[i:i+8, j:j+8], qTable, 5)

        # Calculate inverse DCT
        cr2_dct[i:i+8, j:j+8] = iBlockDCT(cr2_dct[i:i+8, j:j+8])
        cb2_dct[i:i+8, j:j+8] = iBlockDCT(cb2_dct[i:i+8, j:j+8])


# Convert back to RGB
r1_new, g1_new, b1_new = convert2rgb(y1_dct, cr1_dct, cb1_dct, subimg1)
r2_new, g2_new, b2_new = convert2rgb(y2_dct, cr2_dct, cb2_dct, subimg2)

r1_new_img = Image.fromarray(r1_new, 'L')
g1_new_img = Image.fromarray(g1_new, 'L')
b1_new_img = Image.fromarray(b1_new, 'L')

r2_new_img = Image.fromarray(r2_new, 'L')
g2_new_img = Image.fromarray(g2_new, 'L')
b2_new_img = Image.fromarray(b2_new, 'L')

new_image1 = Image.merge("RGB", (r1_new_img, g1_new_img, b1_new_img))
new_image2 = Image.merge("RGB", (r2_new_img, g2_new_img, b2_new_img))

# Show the images
new_image1.show()
new_image2.show()
