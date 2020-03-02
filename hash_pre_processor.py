#Pre-Processing Helper Module

#Converts input string into binary
def convert_to_binary(string):
    string = list(string)

    #Convert characters into bits
    for i in range(len(string)):
        string[i] = bin(ord(string[i]))[2:]
        string[i] = '0' * (8 - len(string[i])) + string[i]
    return ''.join(string)


#Converts input string into a bit array (32-bit)
def convert_32bit(string):
    stringLength = 8 * len(string)
    
    string = convert_to_binary(string) + '1'
    string += '0' * ((448 - len(string)) % 512)
    
    stringLength = bin(stringLength)[2:]
    stringLength = '0' * (64 - len(stringLength)) + stringLength

    string += stringLength
    return string


#Converts input string into a bit array (64-bit)
def convert_64bit(string):
    stringLength = 8 * len(string)
    
    string = convert_to_binary(string) + '1'
    string += '0' * ((896 - len(string)) % 1024)
    
    stringLength = bin(stringLength)[2:]
    stringLength = '0' * (128 - len(stringLength)) + stringLength

    string += stringLength
    return string
