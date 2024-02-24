from jpeg_encoder import *
import matplotlib.pyplot as plt

# Load image
img = Image.open("images/lena_color_512.png")
qSacle = [0.1, 0.3, 0.6, 1, 2, 5]

for q in qSacle:
    encodedJPEG = JPEGencode(img, [4, 2, 2], q)
    imgRec = JPEGdecode(encodedJPEG)

    imgRec.save("images/qSacle/lena_q_" + str(q) + ".png")


