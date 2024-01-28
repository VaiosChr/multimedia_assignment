from PIL import Image
import numpy as np
from rgb_to_ycrcb import convert2ycrcb, convert2rgb


# Open the image
image = Image.open("images/baboon.png")
# image = Image.open("lena_color_512.png")

# Convert the image data to numpy arrays
r, g, b = np.array(image.split())
subing = (4, 2, 0)

# Convert to YCrCb with 4:2:2 subsampling
y, cr, cb = convert2ycrcb(r, g, b, subing)

r_new, g_new, b_new = convert2rgb(y, cr, cb, subing)

r_img = Image.fromarray(r_new, 'L')
g_img = Image.fromarray(g_new, 'L')
b_img = Image.fromarray(b_new, 'L')

# Create a new image from the RGB channels
new_image = Image.merge("RGB", (r_img, g_img, b_img))

# Save the new image to a folder
new_image.save("images/new_baboon.png")
# new_image.save("images/new_lena.png")