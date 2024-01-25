import numpy as np
import cv2


def subsamplingParameters(subsampling):
    if subsampling == (4, 4, 4):
        x_factor = 1
        y_factor = 1
    elif subsampling == (4, 2, 2):
        x_factor = 2
        y_factor = 1
    elif subsampling == (4, 2, 0):
        x_factor = 2
        y_factor = 2
    else:
        raise ValueError("Subsampling must be 4:4:4, 4:2:2 or 4:2:0")

    return x_factor, y_factor


def subsamplingCrCb(cr, cb, subing):
    x, y = subsamplingParameters(subing)

    cr = cr[::x, ::y]
    cb = cb[::x, ::y]

    return cr, cb


def upsampleCrCb(cr, cb, subing):
    x, y = subsamplingParameters(subing)

    cr = np.repeat(np.repeat(cr, x, axis=0), y, axis=1)
    cb = np.repeat(np.repeat(cb, x, axis=0), y, axis=1)

    return cr, cb


def convert2ycrcb(r, g, b, subing):
    # Convert RGB to YCrCb
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = 0.5 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cb = 0.5 + 0.5 * r - 0.418688 * g - 0.081312 * b

    # Subsampling
    cr, cb = subsamplingCrCb(cr, cb, subing)

    return y, cr, cb


def convert2rgb(y, cr, cb, subing):
    # Upsample the cr and cb channels
    cr, cb = upsampleCrCb(cr, cb, subing)

    # Perform inverse YCrCb to RGB conversion
    r = y + 1.402 * (cr - 0.5)
    g = y - 0.344136 * (cb - 0.5) - 0.714136 * (cr - 0.5)
    b = y + 1.772 * (cb - 0.5)

    # Clip values to be in the valid range [0, 1]
    r = np.clip(r, 0, 1)
    g = np.clip(g, 0, 1)
    b = np.clip(b, 0, 1)

    return r, g, b