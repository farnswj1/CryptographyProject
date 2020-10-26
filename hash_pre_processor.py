# Pre-Processing Helper Module

# Converts input string into a binary string
def convert_to_binary(string):
    return ''.join([bin(ord(char))[2:].zfill(8) for char in string])


# Converts input string into a bit array (32-bit)
def convert_32bit(string):
    # Get the number of bits in the string mod (2**64)
    original_string_length = (8 * len(string)) % (2 ** 64)

    # Append a 1 to the binary string of the input string    
    string = convert_to_binary(string) + '1'

    # Pad the binary string with 0's until it is 64 characters short of a multiple of 512
    string += '0' * ((448 - len(string)) % 512)
    
    # Pad the original string length in bits so that it's 64 characters long
    padding = bin(original_string_length)[2:].zfill(64)

    # Return the pre-processed string
    return string + padding


# Converts input string into a bit array (64-bit)
def convert_64bit(string):
    # Get the number of bits in the string mod (2**128)
    original_string_length = (8 * len(string)) % (2 ** 128)
    
    # Append a 1 to the binary string of the input string 
    string = convert_to_binary(string) + '1'

    # Pad the binary string with 0's until it is 64 characters short of a multiple of 1024
    string += '0' * ((896 - len(string)) % 1024)
    
    # Pad the original string length in bits so that it's 128 characters long
    padding = bin(original_string_length)[2:].zfill(128)
    
    # Return the pre-processed string
    return string + padding
