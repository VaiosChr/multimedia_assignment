from collections import Counter
from jpeg_encoder import *

import numpy as np
from PIL import Image

# Calculate the entropy in the RGB spatial domain
def entropy(img):
    hist = np.histogram(img.flatten(), 256, [0, 256])[0]
    hist = hist[hist > 0]
    prob = hist / np.sum(hist)
    return -np.sum(prob * np.log2(prob))


def calculate_entropy(dct_coefficients):
    # Flatten the 8x8 blocks
    flattened_coefficients = dct_coefficients.flatten()
    
    # Calculate probability distribution
    total_coefficients = len(flattened_coefficients)
    probabilities = [count / total_coefficients for count in Counter(flattened_coefficients).values()]
    
    # Compute entropy
    entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
    
    return entropy


def calculate_entropy_rle(rle_coefficients):
    # Flatten the run-length encoded coefficients
    flattened_coefficients = [item for sublist in rle_coefficients for item in sublist]
    
    # Calculate probability distribution
    total_coefficients = len(flattened_coefficients)
    probabilities = [count / total_coefficients for count in Counter(flattened_coefficients).values()]
    
    # Compute entropy
    entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
    
    return entropy


# Baboon image
img1 = Image.open("images/baboon.png")
subimg1 = [4, 2, 2]
qScale1 = 0.6
jpeg1_enc = JPEGencode(img1, subimg1, qScale1)
img1_rec = JPEGdecode(jpeg1_enc)

# Lena image
img2 = Image.open("images/lena_color_512.png")
subimg2 = [4, 4, 4]
qScale2 = 5
jpeg2_enc = JPEGencode(img2, subimg2, qScale2)
img2_rec = JPEGdecode(jpeg2_enc)


######### QUESTION 1 #########

# # Calculate the entropy
entropy1 = entropy(np.array(img1))
entropy2 = entropy(np.array(img2))

# Calculate the entropy of the reconstructed images
entropy1_rec = entropy(np.array(img1_rec))
entropy2_rec = entropy(np.array(img2_rec))

# Print the results
print("Entropy of the original baboon image: ", entropy1)
print("Entropy of the reconstructed baboon image: ", entropy1_rec)
print("Entropy of the original lena image: ", entropy2)
print("Entropy of the reconstructed lena image: ", entropy2_rec)


######### QUESTION 2 #########

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

y1_q_dct = np.zeros(y1.shape)
cr1_q_dct = np.zeros(cr1.shape)
cb1_q_dct = np.zeros(cb1.shape)

y2_q_dct = np.zeros(y2.shape)
cr2_q_dct = np.zeros(cr2.shape)
cb2_q_dct = np.zeros(cb2.shape)

# Break the components in 8x8 blocks
# For luminance components
for i in range(0, y1.shape[0], 8):
    for j in range(0, y1.shape[1], 8):
        y1_q_dct[i:i+8, j:j+8] = blockDCT(y1[i:i+8, j:j+8])
        y2_q_dct[i:i+8, j:j+8] = blockDCT(y2[i:i+8, j:j+8])
        # Quantize the coefficients
        y1_q_dct[i:i+8, j:j+8] = quantizeJPEG(y1_q_dct[i:i+8, j:j+8], qTableL, qScale1)
        y2_q_dct[i:i+8, j:j+8] = quantizeJPEG(y2_q_dct[i:i+8, j:j+8], qTableL, qScale2)


# For chrominance components
for i in range(0, cr1.shape[0], 8):
    for j in range(0, cr1.shape[1], 8):
        # Calculate DCT
        cr1_q_dct[i:i+8, j:j+8] = blockDCT(cr1[i:i+8, j:j+8])
        cb1_q_dct[i:i+8, j:j+8] = blockDCT(cb1[i:i+8, j:j+8])
        # Quantize the coefficients
        cr1_q_dct[i:i+8, j:j+8] = quantizeJPEG(cr1_q_dct[i:i+8, j:j+8], qTableC, qScale1)
        cb1_q_dct[i:i+8, j:j+8] = quantizeJPEG(cb1_q_dct[i:i+8, j:j+8], qTableC, qScale1)

for i in range(0, cr2.shape[0], 8):
    for j in range(0, cr2.shape[1], 8):
        # Calculate DCT
        cr2_q_dct[i:i+8, j:j+8] = blockDCT(cr2[i:i+8, j:j+8])
        cb2_q_dct[i:i+8, j:j+8] = blockDCT(cb2[i:i+8, j:j+8])
        # Quantize the coefficients
        cr2_q_dct[i:i+8, j:j+8] = quantizeJPEG(cr2_q_dct[i:i+8, j:j+8], qTableC, qScale2)
        cb2_q_dct[i:i+8, j:j+8] = quantizeJPEG(cb2_q_dct[i:i+8, j:j+8], qTableC, qScale2)


# Calculate the entropy of the quantized DCT coefficients
entropy_y1_q_dct = calculate_entropy(y1_q_dct)
entropy_cr1_q_dct = calculate_entropy(cr1_q_dct)
entropy_cb1_q_dct = calculate_entropy(cb1_q_dct)

entropy_y2_q_dct = calculate_entropy(y2_q_dct)
entropy_cr2_q_dct = calculate_entropy(cr2_q_dct)
entropy_cb2_q_dct = calculate_entropy(cb2_q_dct)

# Print the results
print("Entropy of the quantized DCT coefficients for the baboon image: ")
print("Y: ", entropy_y1_q_dct)
print("Cr: ", entropy_cr1_q_dct)
print("Cb: ", entropy_cb1_q_dct)
print("Entropy of the quantized DCT coefficients for the lena image: ")
print("Y: ", entropy_y2_q_dct)
print("Cr: ", entropy_cr2_q_dct)
print("Cb: ", entropy_cb2_q_dct)


######### QUESTION 3 #########

y1_rle = []
cr1_rle = []
cb1_rle = []

y2_rle = []
cr2_rle = []
cb2_rle = []

for i in range(0, y1.shape[0], 8):
    DCpred1 = 0
    DCpred2 = 0
    for j in range(0, y1.shape[1], 8):
        y1_rle.append(runLength(y1_q_dct[i:i+8, j:j+8], DCpred1))
        y2_rle.append(runLength(y2_q_dct[i:i+8, j:j+8], DCpred2))

        DCpred1 = y1_rle[-1][0][1]
        DCpred2 = y2_rle[-1][0][1]

for i in range(0, cr1.shape[0], 8):
    DCpred1 = 0
    for j in range(0, cr1.shape[1], 8):
        cr1_rle.append(runLength(cr1_q_dct[i:i+8, j:j+8], DCpred1))
        cb1_rle.append(runLength(cb1_q_dct[i:i+8, j:j+8], DCpred1))

        DCpred1 = cr1_rle[-1][0][1]

for i in range(0, cr2.shape[0], 8):
    DCpred2 = 0
    for j in range(0, cr2.shape[1], 8):
        cr2_rle.append(runLength(cr2_q_dct[i:i+8, j:j+8], DCpred2))
        cb2_rle.append(runLength(cb2_q_dct[i:i+8, j:j+8], DCpred2))

        DCpred2 = cr2_rle[-1][0][1]

# Calculate the entropy of the run-length encoded coefficients
entropy_y1_rle = calculate_entropy_rle(y1_rle)
entropy_cr1_rle = calculate_entropy_rle(cr1_rle)
entropy_cb1_rle = calculate_entropy_rle(cb1_rle)

entropy_y2_rle = calculate_entropy_rle(y2_rle)
entropy_cr2_rle = calculate_entropy_rle(cr2_rle)
entropy_cb2_rle = calculate_entropy_rle(cb2_rle)

# Print the results
print("Entropy of the run-length encoded coefficients for the baboon image: ")
print("Y: ", entropy_y1_rle)
print("Cr: ", entropy_cr1_rle)
print("Cb: ", entropy_cb1_rle)
print("Entropy of the run-length encoded coefficients for the lena image: ")
print("Y: ", entropy_y2_rle)
print("Cr: ", entropy_cr2_rle)
print("Cb: ", entropy_cb2_rle)