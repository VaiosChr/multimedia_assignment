from huffman import huffEnc, huffDec
from transformations.quantization import quantizeJPEG, dequantizeJPEG
from transformations.dct import blockDCT, iBlockDCT
from transformations.zig_zag import runLength, iRunLength
from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
from tables.huffman_tables import *
from tables.quantization_tables import *


img = Image.open('images/baboon.png')

subimg = [4, 4, 4]
r, g, b = np.array(img.split())

y, cr, cb = convert2ycrcb(r, g, b, subimg)

y_new = np.zeros(y.shape)
cr_new = np.zeros(cr.shape)
cb_new = np.zeros(cb.shape)

for i in range(0, y.shape[0], 8):
    DCpred = 0
    for j in range(0, y.shape[1], 8):
        block = y[i:i+8, j:j+8]
        dct_blk = blockDCT(block)
        quant_blk = quantizeJPEG(dct_blk, qTableL, 1)
        runSymbols = runLength(quant_blk, DCpred)
        huffStream = huffEnc(runSymbols)

        runSymbols = huffDec(huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        dct_blk = dequantizeJPEG(quant_blk, qTableL, 1)
        idct_blk = iBlockDCT(dct_blk)
        y_new[i:i+8, j:j+8] = idct_blk

        DCpred = runSymbols[0][1]

for i in range(0, cr.shape[0], 8):
    DCpred = 0
    for j in range(0, cr.shape[1], 8):
        block = cr[i:i+8, j:j+8]
        dct_blk = blockDCT(block)
        quant_blk = quantizeJPEG(dct_blk, qTableC, 1)
        runSymbols = runLength(quant_blk, DCpred)
        huffStream = huffEnc(runSymbols)

        runSymbols = huffDec(huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        dct_blk = dequantizeJPEG(quant_blk, qTableC, 1)
        idct_blk = iBlockDCT(dct_blk)
        cr_new[i:i+8, j:j+8] = idct_blk

        DCpred = runSymbols[0][1]

for i in range(0, cb.shape[0], 8):
    DCpred = 0
    for j in range(0, cb.shape[1], 8):
        block = cb[i:i+8, j:j+8]
        dct_blk = blockDCT(block)
        quant_blk = quantizeJPEG(dct_blk, qTableC, 1)
        runSymbols = runLength(quant_blk, DCpred)
        huffStream = huffEnc(runSymbols)

        runSymbols = huffDec(huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        dct_blk = dequantizeJPEG(quant_blk, qTableC, 1)
        idct_blk = iBlockDCT(dct_blk)
        cb_new[i:i+8, j:j+8] = idct_blk

        DCpred = runSymbols[0][1]
        
r_new, g_new, b_new = convert2rgb(y_new, cr_new, cb_new, subimg)

r_new = np.clip(r_new, 0, 255).astype('uint8')
g_new = np.clip(g_new, 0, 255).astype('uint8')
b_new = np.clip(b_new, 0, 255).astype('uint8')

img_new = Image.merge('RGB', (Image.fromarray(r_new), Image.fromarray(g_new), Image.fromarray(b_new)))

img_new.show()

