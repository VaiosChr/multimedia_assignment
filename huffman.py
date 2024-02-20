import math
from tables.huffman_tables import *

# Define reverse dictionaries for huffman tables
dc_luminance_rev = {v: k for k, v in dc_luminance.items()}
dc_chrominance_rev = {v: k for k, v in dc_chrominance.items()}
ac_luminance_rev = {v: k for k, v in ac_luminance.items()}
ac_chrominance_rev = {v: k for k, v in ac_chrominance.items()}

def negativeNumberToBinary(num):
  num_binary = bin(abs(num-1))[2:]
  num_binary = num_binary.replace('0', '2').replace('1', '0').replace('2', '1')
  # Add 1 to num_binary
  for i in range(len(num_binary)-1, -1, -1):
    if num_binary[i] == '0':
      num_binary = num_binary[:i] + '1' + num_binary[i+1:]
      break
    else:
      num_binary = num_binary[:i] + '0' + num_binary[i+1:]
  
  return num_binary


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
  code = dc_luminance[category] if isLuminance else dc_chrominance[category]
  
  # Binary of diff
  if DIFF < 0:
    diff_binary = negativeNumberToBinary(DIFF)
  elif DIFF == 0:
    diff_binary = ""
  else:
    diff_binary = bin(DIFF)[2:]

  return code + diff_binary[len(diff_binary)-category:]


def encodeAC(coefficients, isLuminance):
  ac_codes = ""

  for coef in coefficients:
    category = findCategory(coef[1])
    ac_code = ac_luminance[(coef[0], category)] if isLuminance else ac_chrominance[(coef[0], category)]

    if coef[1] < 0:
      coef_binary = negativeNumberToBinary(coef[1])
    else:
      coef_binary = bin(abs(coef[1]))[2:]
    ac_codes += ac_code + coef_binary[len(coef_binary)-category:]

  # Add end-of-block marker
  ac_codes += ac_luminance[(0, 0)] if isLuminance else ac_chrominance[(0, 0)]

  return ac_codes


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
    if bitStream[0] == '0':
      bitStream = bitStream.replace('0', '2').replace('1', '0').replace('2', '1')
      diff = -(int(bitStream, 2))
    else:
      diff = int(bitStream, 2)
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
    
    if bitStream[0] == '0':
      bitStream = bitStream.replace('0', '2').replace('1', '0').replace('2', '1')
      coef = -int(bitStream, 2)
    else:
      coef = int(bitStream, 2)
    
    symbols.append((run, coef))
    endIndex += category + 1
    index = endIndex - 1

  return symbols 


def huffDec(huffStream, isLuminance=True):
  diff, index = decodeDC(huffStream, isLuminance)
  symbols = decodeAC(huffStream, index, isLuminance)

  decodedSymbols = [(0, diff)]
  for symbol in symbols:
    decodedSymbols.append(symbol) 

  decodedSymbols.append((0, 0))
  return decodedSymbols