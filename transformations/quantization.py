import numpy as np

# Returns the quantization of a DCT block
def quantizeJPEG(dctBlock, qTable, qScale):
    return np.round(dctBlock / (qTable * qScale)).astype(int)


# Returns the dequantization of a quantized block
def dequantizeJPEG(qBlock, qTable, qScale):
    return qBlock * (qTable * qScale)