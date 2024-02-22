import numpy as np

# Returns the zig-zag scan of a matrix
def zigzagScan(matrix):
    rows, cols = len(matrix), len(matrix[0])
    result = []

    for i in range(rows + cols - 1):
        if i % 2 == 0:  # even diagonal
            for j in range(min(i, rows - 1), max(0, i - cols + 1) - 1, -1):
                result.append(matrix[j][i - j])
        else:  # odd diagonal
            for j in range(min(i, cols - 1), max(0, i - rows + 1) - 1, -1):
                result.append(matrix[i - j][j])

    return result


# Returns the inverse zig-zag scan of a list
def iZigzagScan(zigzag):
    rows, cols = 8, 8
    result = np.zeros((rows, cols))

    for i in range(rows + cols - 1):
        if i % 2 == 0:  # even diagonal
            for j in range(min(i, rows - 1), max(0, i - cols + 1) - 1, -1):
                if len(zigzag) == 0:
                    break
                result[j][i - j] = zigzag.pop(0)
        else:  # odd diagonal
            for j in range(min(i, cols - 1), max(0, i - rows + 1) - 1, -1):
                if len(zigzag) == 0:
                    break
                result[i - j][j] = zigzag.pop(0)

    return result


# Returns the run-length encoding of a quantized block
def runLength(qBlock, DCpred):
    zigzag = zigzagScan(qBlock)
    runSymbols = []

    runSymbols.append((0, zigzag[0] - DCpred))

    counter = 0
    for zz in zigzag[1:]:
        if zz == 0:
            counter += 1
        else:
            runSymbols.append((counter, zz))
            counter = 0
        if counter == 15:
            runSymbols.append((15, 0))
            counter = 0

    return runSymbols


# Returns the inverse run-length encoding of a list of run-length symbols
def iRunLength(runSymbols, DCpred):
    zigzag = []
    zigzag.append(DCpred + runSymbols[0][1])
    
    for symbol in runSymbols[1:]:
        for _ in range(symbol[0]):
            zigzag.append(0)
        zigzag.append(symbol[1])
    
    return iZigzagScan(zigzag)