from huffman import huffEnc, huffDec
from transformations.quantization import quantizeJPEG, dequantizeJPEG
from transformations.dct import blockDCT, iBlockDCT
from transformations.zig_zag import runLength, iRunLength
from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
from tables.quantization_tables import *
from tables.huffman_tables import *


img = Image.open('images/baboon.png')

r, g, b = np.array(img.split())
y, cr, cb = convert2ycrcb(r, g, b, [4, 4, 4])

for i in range(0, y.shape[0], 8):
  DCpred = 0
  for j in range(0, y.shape[1], 8):
    quant_blk = quantizeJPEG(blockDCT(y[i:i+8, j:j+8]), qTableL, 0.07)
    runSymbols = runLength(quant_blk, DCpred)
    # print(quant_blk[0][0], runSymbols[0][1])
    DCpred = runSymbols[0][1]
    if abs(DCpred) > 2047:
      print(DCpred)