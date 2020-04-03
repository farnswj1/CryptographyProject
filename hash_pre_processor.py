#Pre-Processing Helper Module

# Converts input string into binary
def convert_to_binary(string):
    string = list(string)

    # Convert characters into bits
    for i in range(len(string)):
        string[i] = bin(ord(string[i]))[2:]
        string[i] = '0' * (8 - len(string[i])) + string[i]
    return ''.join(string)


# Converts input string into a bit array (32-bit)
def convert_32bit(string):
    original_string_length = 8 * len(string)
    
    string = convert_to_binary(string) + '1'
    string += '0' * ((448 - len(string)) % 512)
    
    padding = bin(original_string_length)[2:]
    padding = '0' * (64 - len(padding)) + padding

    return string + padding


# Converts input string into a bit array (64-bit)
def convert_64bit(string):
    original_string_length = 8 * len(string)
    
    string = convert_to_binary(string) + '1'
    string += '0' * ((896 - len(string)) % 1024)
    
    padding = bin(original_string_length)[2:]
    padding = '0' * (128 - len(padding)) + padding

    return string + padding
