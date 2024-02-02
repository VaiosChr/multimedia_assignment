import numpy as np

def quantizeJPEG(dctBlock, qTable, qScale):
    return np.round(dctBlock / (qTable * qScale)).astype(int)


def dequantizeJPEG(qBlock, qTable, qScale):
    return qBlock * (qTable * qScale)
