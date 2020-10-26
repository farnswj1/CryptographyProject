from hash_pre_processor import convert_32bit
from bitwise_rotator import rotate_left_32bit

# The 'Secure Hash Algorithm 1' cryptographic hash function
# Converts a string of 8-bit characters into a 40-hexadecimal value
def encrypt(string):
    # Pre-processing converts input string into a bit array
    string = convert_32bit(string)

    # Variables
    h0 = 1732584193
    h1 = 4023233417
    h2 = 2562383102
    h3 = 271733878
    h4 = 3285377520
    
    # Processing
    # Partition and build bit array into lists of eighty 32-bit binary strings
    for i in range(0, len(string), 512):
        bit_list = [int(string[i+j : i+j+32], 2) for j in range(0, 512, 32)]
            
        for j in range(16, 80):
            bit_list.append(rotate_left_32bit(bit_list[j - 3] ^ bit_list[j - 8] ^ bit_list[j - 14] ^ bit_list[j - 16], 1))
            
        # Hash values
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        
        # Hashing loop
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b & 0xFFFFFFFF) & d)
                k = 1518500249
            elif j < 40:
                f = b ^ c ^ d
                k = 1859775393
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 2400959708
            else:
                f = b ^ c ^ d
                k = 3395469782
            
            temp = (rotate_left_32bit(a, 5) + f + e + k + bit_list[j]) % 4294967296
            e = d
            d = c
            c = rotate_left_32bit(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) % 4294967296
        h1 = (h1 + b) % 4294967296
        h2 = (h2 + c) % 4294967296
        h3 = (h3 + d) % 4294967296
        h4 = (h4 + e) % 4294967296

    # Convert h-variables into hexadecimal, concatenate them, then return digest
    return ''.join([hex(hvar)[2:].zfill(8) for hvar in (h0, h1, h2, h3, h4)])


# 'A Test' -> 8f0c0855915633e4a7de19468b3874c8901df043
if __name__ == "__main__":
    print(encrypt('A Test') == '8f0c0855915633e4a7de19468b3874c8901df043')
