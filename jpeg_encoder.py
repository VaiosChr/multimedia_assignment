from transformations.huffman import huffEnc
from transformations.quantization import quantizeJPEG
from transformations.dct import blockDCT
from transformations.zig_zag import runLength
from transformations.rgb_to_ycrcb import convert2ycrcb
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
    def __init__(self, blkType, indHor, indVer, huffStream, imgRec):
        self.blkType = blkType          # Type of block (Y, Cb, Cr)
        self.indHor = indHor            # Horizontal index of the block
        self.indVer = indVer            # Vertical index of the block
        self.huffStream = huffStream    # Huffman stream
        self.imgRec = imgRec            # Reconstructed image
        

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
                huffStream = huffStream,
                imgRec = None
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = quant_blk[0, 0]
            
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
                huffStream = huffStream,
                imgRec = None
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = quant_blk[0, 0]
    
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
                huffStream = huffStream,
                imgRec = None
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = quant_blk[0, 0]
                        
    return JPEGenc


img = Image.open('images/baboon.png')
subimg = [4, 2, 2]
qScale = 1
JPEGenc = JPEGencode(img, subimg, qScale)
