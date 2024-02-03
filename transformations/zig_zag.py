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


def runLength(qBlock, DCpred):
    zigzag = zigzagScan(qBlock)
    runSymbols = []

    counter = 0
    runSymbols.append((0, zigzag[0] - DCpred))
    for i in range(1, len(zigzag)):
        if zigzag[i] == 0:
            counter += 1
        else:
            runSymbols.append((counter, zigzag[i]))
            counter = 0
        if counter == 15:
            runSymbols.append((15, 0))
            counter = 0
    runSymbols.append((0, 0))

    return runSymbols


def iRunLength(runSymbols, DCpred):
    zigzag = []
    zigzag.append(DCpred + runSymbols[0][1])

    for i in range(1, len(runSymbols)):
        for j in range(runSymbols[i][0]):
            zigzag.append(0)
        zigzag.append(runSymbols[i][1])
    
    return iZigzagScan(zigzag)


# matrix = np.random.randint(0, 10, size=(8, 8))

# for i in range(len(matrix)):
#     for j in range(len(matrix[0])):
#         if matrix[i][j] < 5:
#             matrix[i][j] = 0

# print(matrix)

# print(runLength(matrix, -5))

# print(iRunLength(runLength(matrix, -5), -5))


