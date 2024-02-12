import math
from tables.huffman_tables import *


dc_luminance_rev = {v: k for k, v in dc_luminance.items()}
dc_chrominance_rev = {v: k for k, v in dc_chrominance.items()}
ac_luminance_rev = {v: k for k, v in ac_luminance.items()}
ac_chrominance_rev = {v: k for k, v in ac_chrominance.items()}

def findCategory(DIFF):
  if DIFF == 0:
    return 0
  
  return (int)(math.log2(abs(DIFF))+1)


def findBase(category):
  if category == 0:
    return 0
  
  return (int)(math.pow(2, category-1))


def huffEnc(runSymbols, isLuminance=True):
  diff = runSymbols[0][1]
  dc_code = encodeDC(diff, isLuminance)

  ac_coefficients = runSymbols[1:]
  ac_codes = encodeAC(ac_coefficients, isLuminance)

  return dc_code + ac_codes


def encodeDC(DIFF, isLuminance):
  category = findCategory(DIFF)
  if isLuminance:
    code = dc_luminance[category]
  else:
    code = dc_chrominance[category]
  
  # Binary of diff
  if DIFF < 0:
    diff_binary = bin(abs(DIFF-1))[2:]
    diff_binary = diff_binary.replace('0', '2').replace('1', '0').replace('2', '1')
    # Add 1 to diff_binary
    for i in range(len(diff_binary)-1, -1, -1):
      if diff_binary[i] == '0':
        diff_binary = diff_binary[:i] + '1' + diff_binary[i+1:]
        break
      else:
        diff_binary = diff_binary[:i] + '0' + diff_binary[i+1:]
  else:
    diff_binary = bin(DIFF)[2:]

  diff_binary = diff_binary[len(diff_binary)-category:]
  print(code, "+", diff_binary)
  return code + diff_binary


def encodeAC(coefficients, isLuminance):
  ac_codes = ""

  for coef in coefficients:
    category = findCategory(coef[1])
    ac_code = ac_luminance[(coef[0], category)] if isLuminance else ac_chrominance[(coef[0], category)]
    if coef[1] < 0:
      coef_binary = bin(abs(coef[1]-1))[2:]
      coef_binary = coef_binary.replace('0', '2').replace('1', '0').replace('2', '1')
      # Add 1 to diff_binary
      for i in range(len(coef_binary)-1, -1, -1):
        if coef_binary[i] == '0':
          coef_binary = coef_binary[:i] + '1' + coef_binary[i+1:]
          break
    else:
      coef_binary = '0' + bin(abs(coef[1]))[2:]
    ac_codes += ac_code + coef_binary[len(coef_binary)-category:]

  # Add end-of-block marker
  ac_codes += ac_luminance[(0, 0)] if isLuminance else ac_chrominance[(0, 0)]

  return ac_codes


def decodeDC(huffStream, isLuminance):
  endIndex = 1
  
  while endIndex < len(huffStream):
    try:
      category = dc_luminance_rev[huffStream[:endIndex]] if isLuminance else dc_chrominance_rev[huffStream[:endIndex]]
    except:
      endIndex += 1
      continue
    
    if category == 0:
      return 0, endIndex + 1
    
    bit = huffStream[endIndex:endIndex+category]
    if bit[0] == '0':
      bit = bit.replace('0', '2').replace('1', '0').replace('2', '1')
      diff = -(int(bit, 2))
    else:
      diff = int(bit, 2)
    return diff, endIndex + category


def decodeAC(huffStream, index, isLuminance):
  endIndex = index + 1
  symbols = []

  while endIndex < len(huffStream):
    try:
      run, category = ac_luminance_rev[huffStream[index:endIndex]] if isLuminance else ac_chrominance_rev[huffStream[index:endIndex]]
    except:
      endIndex += 1
      continue

    base = findBase(category)
    bit = huffStream[endIndex:endIndex+category]
    if bit[0] == '0':
      bit = bit.replace('0', '2').replace('1', '0').replace('2', '1')
      coef = -int(bit, 2)
    else:
      coef = int(bit, 2)
    
    symbols.append((run, coef))
    endIndex += category + 1
    index = endIndex - 1

  return symbols 

def huffDec(huffStream, isLuminance=True):
  diff, index = decodeDC(huffStream, isLuminance)
  symbols = decodeAC(huffStream, index, isLuminance)

  decodedSymbols = [(0, diff)]
  decodedSymbols.append(symbols)

  return decodedSymbols

# Example RLE data for the given block
runSymbols = [(0, -1), (1, 1), (2, 5), (0, 1), (3, 2), (1, 6)]

encoded_block = huffEnc(runSymbols)

print("Encoded Block:", encoded_block)
  
decoded_block = huffDec(encoded_block)
print("Decoded Block:", decoded_block)

#@TODO: EOB code remains