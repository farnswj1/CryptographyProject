#Checks if the string consists of only 8-bit characters
def is_8bit(string):
    for i in string:
        if ord(i) >= 128:
            return False
    return True
