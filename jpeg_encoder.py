from huffman import huffEnc, huffDec
from transformations.quantization import quantizeJPEG, dequantizeJPEG
from transformations.dct import blockDCT, iBlockDCT
from transformations.zig_zag import runLength, iRunLength
from transformations.rgb_to_ycrcb import convert2ycrcb, convert2rgb
from PIL import Image
from tables.huffman_tables import *
from tables.quantization_tables import *

# JPEGenc first element
class JPEGfirst:
    def __init__(self):
        self.qTableL = qTableL          # Quantization table for luminance
        self.qTableC = qTableC          # Quantization table for chrominance
        self.DCL = dc_luminance         # Elements used to encode the DC coefficients for luminance block
        self.DCC = dc_chrominance       # Elements used to encode the DC coefficients for chrominance block
        self.ACL = ac_luminance         # Elements used to encode the AC coefficients for luminance block
        self.ACC = ac_chrominance       # Elements used to encode the AC coefficients for chrominance block


# JPEGenc block item
class JPEGblockItem:
    def __init__(self, blkType, indHor, indVer, huffStream):
        self.blkType = blkType          # Type of block (Y, Cb, Cr)
        self.indHor = indHor            # Horizontal index of the block
        self.indVer = indVer            # Vertical index of the block
        self.huffStream = huffStream    # Huffman stream
        

# JPEG encode the image
def JPEGencode(img, subimg, qScale):
    JPEGenc = (JPEGfirst(),)
    
    r, g, b = np.array(img.split())
    y, cr, cb = convert2ycrcb(r, g, b, subimg)
    
    # Luminance block encoding
    for i in range(0, y.shape[0], 8):
        DCpred = 0
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
                indHor = j,
                indVer = i,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
            
    # Chrominance block encoding
    ### Cr
    for i in range(0, cr.shape[0], 8):
        DCpred = 0
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
                indHor = j,
                indVer = i,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
    
    ### Cb
    for i in range(0, cb.shape[0], 8):
        DCpred = 0
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
                indHor = j,
                indVer = i,
                huffStream = huffStream
            )
            # Store the block item
            JPEGenc += (blkItem,)
            DCpred = runSymbols[0][1]
                        
    return JPEGenc


# JPEG decode the image
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

    # Sort the blocks by their indices
    y_JPEGenc.sort(key=lambda x: (x.indVer, x.indHor))
    cr_JPEGenc.sort(key=lambda x: (x.indVer, x.indHor))
    cb_JPEGenc.sort(key=lambda x: (x.indVer, x.indHor))

    y = np.empty((y_JPEGenc[-1].indVer+8, y_JPEGenc[-1].indHor+8))
    cr = np.empty((cr_JPEGenc[-1].indVer+8, cr_JPEGenc[-1].indHor+8))
    cb = np.empty((cb_JPEGenc[-1].indVer+8, cb_JPEGenc[-1].indHor+8))

    # Luminance block decoding
    for blk in y_JPEGenc:
        if blk.indHor == 0:
            DCpred = 0
        else:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(blk.huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableL, qScale)
        # Inverse DCT
        final_block = iBlockDCT(quant_blk)
        y[blk.indVer:blk.indVer+8, blk.indHor:blk.indHor+8] = final_block

    # Chrominance block decoding
    ## Cr
    for blk in cr_JPEGenc:
        if blk.indHor == 0:
            DCpred = 0
        else:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(blk.huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableC, qScale)
        # Inverse DCT
        final_block = iBlockDCT(quant_blk)
        cr[blk.indVer:blk.indVer+8, blk.indHor:blk.indHor+8] = final_block

    ## Cb
    for blk in cb_JPEGenc:
        if blk.indHor == 0:
            DCpred = 0
        else:
            DCpred = runSymbols[0][1]
        # Huffman decode the block
        runSymbols = huffDec(blk.huffStream)
        quant_blk = iRunLength(runSymbols, DCpred)
        # Dequantize the block
        quant_blk = dequantizeJPEG(quant_blk, JPEGenc[0].qTableC, qScale)
        # Inverse DCT
        final_block = iBlockDCT(quant_blk)
        cb[blk.indVer:blk.indVer+8, blk.indHor:blk.indHor+8] = final_block
            
    return mergeRGB(y, cr, cb)


# Merge the Y, Cr, and Cb into an image
def mergeRGB(y, cr, cb):
    # Calculate sumsampling matrix
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
subimg = [4, 2, 0]
qScale = 0.08
JPEGenc = JPEGencode(img, subimg, qScale)
img = JPEGdecode(JPEGenc)
img.show()

# img.save('images/baboon_jpeg.png')

# img = Image.open('images/lena_color_512.png')
# subimg = [4, 4, 4]
# qScale = 0.1
# JPEGenc = JPEGencode(img, subimg, qScale)
# img = JPEGdecode(JPEGenc)
# img.show()

# img.save('images/lena_jpeg.png')


