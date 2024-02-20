from huffman import huffEnc, huffDec
from transformations.quantization import quantizeJPEG, dequantizeJPEG
from transformations.dct import blockDCT, iBlockDCT
from transformations.zig_zag import runLength, iRunLength
from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
from tables.huffman_tables import *
from tables.quantization_tables import *

class JPEGfirst:
    def __init__(self):
        self.qTableL = qTableL          # Quantization table for luminance
        self.qTableC = qTableC          # Quantization table for chrominance
        self.DCL = dc_luminance         # Elements used to encode the DC coefficients for luminance block
        self.DCC = dc_chrominance       # Elements used to encode the DC coefficients for chrominance block
        self.ACL = ac_luminance         # Elements used to encode the AC coefficients for luminance block
        self.ACC = ac_chrominance       # Elements used to encode the AC coefficients for chrominance block


class JPEGblockItem:
    def __init__(self, blkType, indHor, indVer, huffStream):
        self.blkType = blkType          # Type of block (Y, Cb, Cr)
        self.indHor = indHor            # Horizontal index of the block
        self.indVer = indVer            # Vertical index of the block
        self.huffStream = huffStream    # Huffman stream
        

def JPEGencode(img, subimg, qScale):
    JPEGenc = (JPEGfirst(),)
    
    r, g, b = np.array(img.split())
    y, cr, cb = convert2ycrcb(r, g, b, subimg)
    
    DCpred = 0
    
    # Luminance block encoding
    for i in range(0, y.shape[0], 8):
        for j in range(0, y.shape[1], 8):
            # Extract the block
            block = y[i:i+8, j:j+8]
            # Perform DCT
            dct_blk = blockDCT(block)
            # Quantize the block
            quant_blk = quantizeJPEG(dct_blk, JPEGenc[0].qTableL, qScale)
            # Run-length encode the block
            runSymbols = runLength(quant_blk, DCpred)
            # Huffman encode the block
            huffStream = huffEnc(runSymbols)
            # Store the huffman stream
            blkItem = JPEGblockItem(
                blkType = "Y",
                indHor = i,
                indVer = j,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
            
    # Chrominance block encoding
    ### Cr
    DCpred = 0
    for i in range(0, cr.shape[0], 8):
        for j in range(0, cr.shape[1], 8):
            # Extract the block
            block = cr[i:i+8, j:j+8]
            # Perform DCT
            dct_blk = blockDCT(block)
            # Quantize the block
            quant_blk = quantizeJPEG(dct_blk, JPEGenc[0].qTableC, qScale)
            # Run-length encode the block
            runSymbols = runLength(quant_blk, DCpred)
            # Huffman encode the block
            huffStream = huffEnc(runSymbols)
            # Store the huffman stream
            blkItem = JPEGblockItem(
                blkType = "Cr",
                indHor = i,
                indVer = j,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
    
    ### Cb
    DCpred = 0
    for i in range(0, cb.shape[0], 8):
        for j in range(0, cb.shape[1], 8):
            # Extract the block
            block = cb[i:i+8, j:j+8]
            # Perform DCT
            dct_blk = blockDCT(block)
            # Quantize the block
            quant_blk = quantizeJPEG(dct_blk, JPEGenc[0].qTableC, qScale)
            # Run-length encode the block
            runSymbols = runLength(quant_blk, DCpred)
            # Huffman encode the block
            huffStream = huffEnc(runSymbols)
            # Store the huffman stream
            blkItem = JPEGblockItem(
                blkType = "Cb",
                indHor = i,
                indVer = j,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
                        
    return JPEGenc


def JPEGdecode(JPEGenc):
    y_JPEGenc = []
    cr_JPEGenc = []
    cb_JPEGenc = []


    # Split the JPEGenc into Y, Cr, and Cb
    for i in range(1, len(JPEGenc)):
        if JPEGenc[i].blkType == "Y":
            y_JPEGenc.append(JPEGenc[i])
        elif JPEGenc[i].blkType == "Cr":
            cr_JPEGenc.append(JPEGenc[i])
        elif JPEGenc[i].blkType == "Cb":
            cb_JPEGenc.append(JPEGenc[i])
    
    y = np.empty((y_JPEGenc[-1].indHor+8, y_JPEGenc[-1].indVer+8))
    cr = np.empty((cr_JPEGenc[-1].indHor+8, cr_JPEGenc[-1].indVer+8))
    cb = np.empty((cb_JPEGenc[-1].indHor+8, cb_JPEGenc[-1].indVer+8))

    # Luminance block decoding
    DCpred = 0
    runSymbols = huffDec(y_JPEGenc[0].huffStream)
    for i in range(len(y_JPEGenc)):
        if i > 0:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(y_JPEGenc[i].huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableL, qScale)
        # Inverse DCT
        block = iBlockDCT(quant_blk)
        y[y_JPEGenc[i].indHor:y_JPEGenc[i].indHor+8, y_JPEGenc[i].indVer:y_JPEGenc[i].indVer+8] = block
            
    # Chrominance block decoding
    ### Cr
    DCpred = 0
    runSymbols = huffDec(cr_JPEGenc[0].huffStream)
    for i in range(len(cr_JPEGenc)):
        if i > 0:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(cr_JPEGenc[i].huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableC, qScale)
        # Inverse DCT
        block = iBlockDCT(quant_blk)
        # Store the reconstructed block
        cr[cr_JPEGenc[i].indHor:cr_JPEGenc[i].indHor+8, cr_JPEGenc[i].indVer:cr_JPEGenc[i].indVer+8] = block

    ### Cb
    DCpred = 0
    runSymbols = huffDec(cb_JPEGenc[0].huffStream)
    for i in range(len(cb_JPEGenc)):
        if i > 0:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(cb_JPEGenc[i].huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableC, qScale)
        # Inverse DCT
        block = iBlockDCT(quant_blk)
        # Store the reconstructed block
        cb[cb_JPEGenc[i].indHor:cb_JPEGenc[i].indHor+8, cb_JPEGenc[i].indVer:cb_JPEGenc[i].indVer+8] = block
            
    return mergeRGB(y, cr, cb)

def mergeRGB(y, cr, cb):
    # Calculate sumsampling parameters
    subimg = [4, 4, 4]
    if y.shape[1]//cr.shape[1] == 2:
        subimg = [4, 2, 2]
    if y.shape[0]//cr.shape[0] == 2:
        subimg = [4, 2, 0]
    
    # Convert YCrCb to RGB
    r, g, b = convert2rgb(y, cr, cb, subimg)

    # Create the image
    r_img = Image.fromarray(r, 'L')
    g_img = Image.fromarray(g, 'L')
    b_img = Image.fromarray(b, 'L')

    return Image.merge("RGB", (r_img, g_img, b_img))


img = Image.open('images/baboon.png')
subimg = [4, 2, 2]
qScale = 1
JPEGenc = JPEGencode(img, subimg, qScale)
img = JPEGdecode(JPEGenc)
img.show()

# img.save('images/baboon_jpeg.png')


