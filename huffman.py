from huffman_tables import dc_luminance, dc_chrominance, ac_luminance, ac_chrominance
import math

def findCategory(DIFF):
  if DIFF == 0:
    return 0
  
  return (int)(math.log2(abs(DIFF))+1)



# def huffEnc(runSymbols, isLuminance=True):
#   huffStream = ""

#   if isLuminance:
#     huffStream += dc_luminance[abs(runSymbols[0][1])]

#     for i in range(1, len(runSymbols)):
#       huffStream += ac_luminance[runSymbols[i][0], abs(runSymbols[i][1])]
#   else: 
#     huffStream += dc_chrominance[abs(runSymbols[0][1])]

#     for i in range(1, len(runSymbols)):
#       huffStream += ac_chrominance[runSymbols[i][0], abs(runSymbols[i][1])]
  
#   return huffStream


# def huffDec(huffStream, isLuminance=True):
#     index = 0
#     endIndex = 1
#     decodedSymbols = []

#     dc_luminance_rev = {v: k for k, v in dc_luminance.items()}
#     dc_chrominance_rev = {v: k for k, v in dc_chrominance.items()}
#     ac_luminance_rev = {v: k for k, v in ac_luminance.items()}
#     ac_chrominance_rev = {v: k for k, v in ac_chrominance.items()}
#     print(ac_luminance_rev["1010"])

#     while index < len(huffStream):
#       try:
#         if isLuminance:
#           symbol = dc_luminance_rev[huffStream[index:endIndex]]
#         else:
#           symbol = dc_chrominance_rev[huffStream[index:endIndex]]
#       except:
#         endIndex += 1
#         continue
#       decodedSymbols.append((0, symbol))
#       index = endIndex
#       endIndex += 1
#       break    

#     while index < len(huffStream):
#       try:
#         if isLuminance:
#           run, size = ac_luminance_rev[huffStream[index:endIndex]]
#         else:
#           run, size = ac_chrominance_rev[huffStream[index:endIndex]]
#       except:
#         endIndex += 1
#         continue
#       decodedSymbols.append((run, size))

#       index = endIndex
#       endIndex += 1

#     return decodedSymbols

# # Example usage:
# runSymbols = [(0, 5), (1, 3), (2, 5), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0), (3, 2), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 6)]
# encodedStream = huffEnc(runSymbols)
# # print(encodedStream)
# decodedSymbols = huffDec(encodedStream)
# print(decodedSymbols)

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
  
  # binary of diff
  if DIFF < 0:
    diff_binary = bin(abs(DIFF-1))[2:]
    diff_binary = diff_binary.replace('0', '2').replace('1', '0').replace('2', '1')
    # add 1 to diff_binary
    for i in range(len(diff_binary)-1, -1, -1):
      if diff_binary[i] == '0':
        diff_binary = diff_binary[:i] + '1' + diff_binary[i+1:]
        break
      else:
        diff_binary = diff_binary[:i] + '0' + diff_binary[i+1:]
  else:
    diff_binary = bin(abs(DIFF))[2:]

  return code


def encodeAC(coefficients, isLuminance):
  ac_codes = ""

  for coef in coefficients:
    if isLuminance:
      ac_code = ac_luminance[coef]
    else:
      ac_code = ac_chrominance[coef]
    ac_codes += ac_code

  # Add end-of-block marker
  if isLuminance:
    ac_codes += ac_luminance[(0, 0)]
  else:
    ac_codes += ac_chrominance[(0, 0)]

  return ac_codes


def huffDec(huffStream, isLuminance=True):
  index = 0
  endIndex = 1
  decodedSymbols = []

  dc_luminance_rev = {v: k for k, v in dc_luminance.items()}
  dc_chrominance_rev = {v: k for k, v in dc_chrominance.items()}
  ac_luminance_rev = {v: k for k, v in ac_luminance.items()}
  ac_chrominance_rev = {v: k for k, v in ac_chrominance.items()}

  while index < len(huffStream):
    try:
      if isLuminance:
        symbol = dc_luminance_rev[huffStream[index:endIndex]]
      else:
        symbol = dc_chrominance_rev[huffStream[index:endIndex]]
    except:
      endIndex += 1
      continue
    decodedSymbols.append((0, symbol))
    index = endIndex
    endIndex += 1
    break    

  while index < len(huffStream):
    try:
      if isLuminance:
        run, size = ac_luminance_rev[huffStream[index:endIndex]]
      else:
        run, size = ac_chrominance_rev[huffStream[index:endIndex]]
    except:
      endIndex += 1
      continue
    decodedSymbols.append((run, size))

    index = endIndex
    endIndex += 1

  return decodedSymbols

# Example RLE data for the given block
runSymbols = [(0, -42), (1, 3), (2, 5), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0), (3, 2), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 6)]

encoded_block = huffEnc(runSymbols)

print("Encoded Block:", encoded_block)
  
decoded_block = huffDec(encoded_block)
print("Decoded Block:", decoded_block)