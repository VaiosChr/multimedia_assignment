from jpeg_encoder import *
import matplotlib.pyplot as plt

# Load image
img = Image.open("images/baboon.png")
zero = [20, 40, 50, 60, 63]
qScale = 1

# Encode and decode the image
JPEGenc = JPEGencode(img, zero, qScale)
imgRec = JPEGdecode(JPEGenc)

# Save the images
# imgRec.save("images/qTable/baboon_20.png")

  


