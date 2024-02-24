from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
import numpy as np
from transformations.dct import blockDCT, iBlockDCT
from transformations.quantization import quantizeJPEG, dequantizeJPEG
from tables.quantization_tables import qTableL, qTableC

######### QUESTION 1 #########

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

# Convert back to RGB
r1_new, g1_new, b1_new = convert2rgb(y1, cr1, cb1, subimg1)
r2_new, g2_new, b2_new = convert2rgb(y2, cr2, cb2, subimg2)

r1_new_img = Image.fromarray(r1_new, 'L')
g1_new_img = Image.fromarray(g1_new, 'L')
b1_new_img = Image.fromarray(b1_new, 'L')

r2_new_img = Image.fromarray(r2_new, 'L')
g2_new_img = Image.fromarray(g2_new, 'L')
b2_new_img = Image.fromarray(b2_new, 'L')

# Create a new image from the RGB channels
new_image1 = Image.merge("RGB", (r1_new_img, g1_new_img, b1_new_img))
new_image2 = Image.merge("RGB", (r2_new_img, g2_new_img, b2_new_img))

# Show the images
new_image1.show()
new_image2.show()

# Save the images
new_image1.save("images/baboon1.png")
new_image2.save("images/lena1.png")


######### QUESTION 2 #########

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

qScale1 = 0.6
qScale2 = 5

y1_new = np.zeros(y1.shape)
cr1_new = np.zeros(cr1.shape)
cb1_new = np.zeros(cb1.shape)

y2_new = np.zeros(y2.shape)
cr2_new = np.zeros(cr2.shape)
cb2_new = np.zeros(cb2.shape)

# Break the components in 8x8 blocks
# For luminance components
for i in range(0, y1.shape[0], 8):
    for j in range(0, y1.shape[1], 8):
        y1_new[i:i+8, j:j+8] = blockDCT(y1[i:i+8, j:j+8])
        y2_new[i:i+8, j:j+8] = blockDCT(y2[i:i+8, j:j+8])

        # Quantize the coefficients
        y1_new[i:i+8, j:j+8] = quantizeJPEG(y1_new[i:i+8, j:j+8], qTableL, qScale1)
        y2_new[i:i+8, j:j+8] = quantizeJPEG(y2_new[i:i+8, j:j+8], qTableL, qScale2)

        # Dequantize the coefficients
        y1_new[i:i+8, j:j+8] = dequantizeJPEG(y1_new[i:i+8, j:j+8], qTableL, qScale1)
        y2_new[i:i+8, j:j+8] = dequantizeJPEG(y2_new[i:i+8, j:j+8], qTableL, qScale2)

        # Calculate inverse DCT
        y1_new[i:i+8, j:j+8] = iBlockDCT(y1_new[i:i+8, j:j+8])
        y2_new[i:i+8, j:j+8] = iBlockDCT(y2_new[i:i+8, j:j+8])

# For chrominance components
for i in range(0, cr1.shape[0], 8):
    for j in range(0, cr1.shape[1], 8):
        # Calculate DCT
        cr1_new[i:i+8, j:j+8] = blockDCT(cr1[i:i+8, j:j+8])
        cb1_new[i:i+8, j:j+8] = blockDCT(cb1[i:i+8, j:j+8])

        # Quantize the coefficients
        cr1_new[i:i+8, j:j+8] = quantizeJPEG(cr1_new[i:i+8, j:j+8], qTableC, qScale1)
        cb1_new[i:i+8, j:j+8] = quantizeJPEG(cb1_new[i:i+8, j:j+8], qTableC, qScale1)

        # Dequantize the coefficients
        cr1_new[i:i+8, j:j+8] = dequantizeJPEG(cr1_new[i:i+8, j:j+8], qTableC, qScale1)
        cb1_new[i:i+8, j:j+8] = dequantizeJPEG(cb1_new[i:i+8, j:j+8], qTableC, qScale1)

        # Calculate inverse DCT
        cr1_new[i:i+8, j:j+8] = iBlockDCT(cr1_new[i:i+8, j:j+8])
        cb1_new[i:i+8, j:j+8] = iBlockDCT(cb1_new[i:i+8, j:j+8])

for i in range(0, cr2.shape[0], 8):
    for j in range(0, cr2.shape[1], 8):
        # Calculate DCT
        cr2_new[i:i+8, j:j+8] = blockDCT(cr2[i:i+8, j:j+8])
        cb2_new[i:i+8, j:j+8] = blockDCT(cb2[i:i+8, j:j+8])

        # Quantize the coefficients
        cr2_new[i:i+8, j:j+8] = quantizeJPEG(cr2_new[i:i+8, j:j+8], qTableC, qScale2)
        cb2_new[i:i+8, j:j+8] = quantizeJPEG(cb2_new[i:i+8, j:j+8], qTableC, qScale2)

        # Dequantize the coefficients
        cr2_new[i:i+8, j:j+8] = dequantizeJPEG(cr2_new[i:i+8, j:j+8], qTableC, qScale2)
        cb2_new[i:i+8, j:j+8] = dequantizeJPEG(cb2_new[i:i+8, j:j+8], qTableC, qScale2)

        # Calculate inverse DCT
        cr2_new[i:i+8, j:j+8] = iBlockDCT(cr2_new[i:i+8, j:j+8])
        cb2_new[i:i+8, j:j+8] = iBlockDCT(cb2_new[i:i+8, j:j+8])


# Convert back to RGB
r1_new, g1_new, b1_new = convert2rgb(y1_new, cr1_new, cb1_new, subimg1)
r2_new, g2_new, b2_new = convert2rgb(y2_new, cr2_new, cb2_new, subimg2)

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

# Save the images
new_image1.save("images/baboon2.png")
new_image2.save("images/lena2.png")
