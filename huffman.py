import math
from tables.huffman_tables import *

# Define reverse dictionaries for huffman tables
dc_luminance_rev = {v: k for k, v in dc_luminance.items()}
dc_chrominance_rev = {v: k for k, v in dc_chrominance.items()}
ac_luminance_rev = {v: k for k, v in ac_luminance.items()}
ac_chrominance_rev = {v: k for k, v in ac_chrominance.items()}

# Convert signed number to binary
def numberToBinary(num):
  if num < 0:
    num_binary = bin(abs(num-1))[2:]
    # Invert bits
    num_binary = num_binary.replace('0', '2').replace('1', '0').replace('2', '1')
    # Add 1 to num_binary
    for i in range(len(num_binary)-1, -1, -1):
      if num_binary[i] == '0':
        num_binary = num_binary[:i] + '1' + num_binary[i+1:]
        break
      else:
        num_binary = num_binary[:i] + '0' + num_binary[i+1:]
  elif num == 0:
    num_binary = ""
  else:
    num_binary = bin(num)[2:]
  
  return num_binary


# Convert binary to signed number
def binaryToNumber(binary):
  if binary[0] == '0':
    binary = binary.replace('0', '2').replace('1', '0').replace('2', '1')
    num = -(int(binary, 2))
  else:
    num = int(binary, 2)
  
  return num


# Find category of a number, according to JPEG standard
def findCategory(DIFF):
  if DIFF == 0:
    return 0
  
  return (int)(math.log2(abs(DIFF))+1)


# Encoding functions
## Encode DC coefficient
def encodeDC(DIFF, isLuminance):
  category = findCategory(DIFF)
  code = dc_luminance[category] if isLuminance else dc_chrominance[category]
  
  diff_binary = numberToBinary(DIFF)

  return code + diff_binary[len(diff_binary)-category:]


## Encode AC coefficients
def encodeAC(coefficients, isLuminance):
  ac_codes = ""

  for coef in coefficients:
    category = findCategory(coef[1])
    if category == 0:
      ac_codes += ac_luminance[(0, 0)] if isLuminance else ac_chrominance[(0, 0)]
      continue
    ac_code = ac_luminance[(coef[0], category)] if isLuminance else ac_chrominance[(coef[0], category)]

    coef_binary = numberToBinary(coef[1])
    ac_codes += ac_code + coef_binary[len(coef_binary)-category:]

  # Add end-of-block marker
  ac_codes += ac_luminance[(0, 0)] if isLuminance else ac_chrominance[(0, 0)]

  return ac_codes


# Decoding functions
## Decode DC coefficient
def decodeDC(huffStream, isLuminance):
  endIndex = 1
  
  while endIndex <= len(huffStream):
    try:
      category = dc_luminance_rev[huffStream[:endIndex]] if isLuminance else dc_chrominance_rev[huffStream[:endIndex]]
      if category == 0:
        return 0, endIndex
    except:
      endIndex += 1
      continue
    
    bitStream = huffStream[endIndex:endIndex+category]
    diff = binaryToNumber(bitStream)

    return diff, endIndex + category
  

## Decode AC coefficients
def decodeAC(huffStream, index, isLuminance):
  endIndex = index + 1
  symbols = []

  while endIndex < len(huffStream):
    try:
      run, category = ac_luminance_rev[huffStream[index:endIndex]] if isLuminance else ac_chrominance_rev[huffStream[index:endIndex]]
    except:
      endIndex += 1
      continue

    if category == 0:
      if run == 0:
        symbols.append((0, 0))
        return symbols
      elif run == 15:
        symbols.append((15, 0))
        endIndex += 1
        index = endIndex
        continue

    bitStream = huffStream[endIndex:endIndex+category]
    coef = binaryToNumber(bitStream)
    
    symbols.append((run, coef))
    endIndex += category + 1
    index = endIndex - 1

  return symbols 


# Main functions
## Huffman encoding of the run-length symbols
def huffEnc(runSymbols, isLuminance=True):
  dc_code = encodeDC(runSymbols[0][1], isLuminance)
  ac_codes = encodeAC(runSymbols[1:], isLuminance)

  return dc_code + ac_codes


## Huffman decoding of the huffman stream
def huffDec(huffStream, isLuminance=True):
  diff, index = decodeDC(huffStream, isLuminance)
  symbols = decodeAC(huffStream, index, isLuminance)

  decodedSymbols = [(0, diff)]
  for symbol in symbols:
    decodedSymbols.append(symbol) 

  decodedSymbols.append((0, 0))
  return decodedSymbols