from PIL import Image
import numpy as np
from rgb_to_ycrcb import convert2ycrcb, convert2rgb


# Open the image
image = Image.open("baboon.png")


# Convert the image data to numpy arrays
r, g, b = np.array(image.split())

# Convert to YCrCb with 4:2:2 subsampling
y, cr, cb = convert2ycrcb(r, g, b, (4, 2, 0))

r_new, g_new, b_new = convert2rgb(y, cr, cb, (4, 2, 0))

r_img = Image.fromarray(r_new.astype('uint8'), 'L')
g_img = Image.fromarray(g_new.astype('uint8'), 'L')
b_img = Image.fromarray(b_new.astype('uint8'), 'L')

# Create a new image from the RGB channels
new_image = Image.merge("RGB", (r_img, g_img, b_img))

# Save the new image to a folder
new_image.save("new_baboon.png")