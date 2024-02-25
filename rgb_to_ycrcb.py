import numpy as np

# Subsampling function: subsamples the cr and cb channels and returns them
def subsampleCrCb(cr, cb, subimg):
    if subimg[2] == 4:
        x, y = 1, 1
    elif subimg[2] == 2:
        x, y = 2, 1
    else: 
        x, y = 2, 2

    cr = cr[::y, ::x]
    cb = cb[::y, ::x]

    return cr, cb


# Upsampling function: upsamples the cr and cb channels and returns them
def upsampleCrCb(cr, cb, subimg):    
    if subimg[1] == 2:
        cr = interpolateColumns(cr)
        cb = interpolateColumns(cb)
        if subimg[2] == 0:
            cr = interpolateRows(cr)
            cb = interpolateRows(cb)

    return cr, cb


# Converts RGB to YCrCb
def convert2ycrcb(r, g, b, subimg):
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b

    cr, cb = subsampleCrCb(cr, cb, subimg)

    return y, cr, cb


# Converts YCrCb to RGB
def convert2rgb(y, cr, cb, subimg):
    # Upsample the cr and cb channels
    cr, cb = upsampleCrCb(cr, cb, subimg)
    
    # Perform inverse YCrCb to RGB conversion
    r = y + 1.402 * cr
    g = y - 0.7141 * cr - 0.3441 * cb
    b = y + 1.772 * cb

    # Clip the values to the range [0, 255]
    r = np.clip(r, 0, 255)
    g = np.clip(g, 0, 255)
    b = np.clip(b, 0, 255)

    return r.astype('uint8'), g.astype('uint8'), b.astype('uint8')
    

# Interpolation functions
# Interpolates the columns of the input array
def interpolateColumns(array):
    rows, cols = array.shape

    interpolated_array = np.zeros((rows, 2 * cols), dtype=array.dtype)
    
    for j in range(cols - 1):
        interpolated_array[:, 2 * j] = array[:, j]
        interpolated_array[:, 2 * j + 1] = (array[:, j] + array[:, j + 1]) / 2.0
    
    return interpolated_array


# Interpolates the rows of the input array
def interpolateRows(array):
    rows, cols = array.shape
    
    interpolated_array = np.zeros((2 * rows, cols), dtype=array.dtype)
    
    for i in range(rows - 1):
        interpolated_array[2 * i, :] = array[i, :]
        interpolated_array[2 * i + 1, :] = (array[i, :] + array[i + 1, :]) / 2.0
    
    return interpolated_array


