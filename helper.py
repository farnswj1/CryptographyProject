# Checks if the string consists of only 8-bit characters
def is_8bit(string):
    # Check if each letter's character code is in the ASCII table
    for char in string:
        if ord(char) >= 128:
            return False
    return True
