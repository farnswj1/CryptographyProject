from hash_pre_processor import convert_32bit
from bitwise_rotator import rotate_left_32bit

# The 'Secure Hash Algorithm 1' cryptographic hash function
# Converts a string of 8-bit characters into a 40-hexadecimal value
def encrypt(string):
    # Pre-processing converts input string into a bit array
    string = convert_32bit(string)

    # Variables
    h1 = 1732584193
    h2 = 4023233417
    h3 = 2562383102
    h4 = 271733878
    h5 = 3285377520
    
    # Processing
    # Partition and build bit array into lists of eighty 32-bit binary strings
    for i in range(len(string) // 512):
        bit_list = []
        partition = string[512 * i : 512 * (i + 1)]
        
        for j in range(0, 512, 32):
            bit_list.append(int(partition[j : j + 32], 2))
            
        for k in range(16, 80):     
            bit_list.append(rotate_left_32bit(bit_list[k - 3] ^ bit_list[k - 8] ^ bit_list[k - 14] ^ bit_list[k - 16], 1))
            
        # Hash values
        a = h1
        b = h2
        c = h3
        d = h4
        e = h5
        
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

        h1 = (h1 + a) % 4294967296
        h2 = (h2 + b) % 4294967296
        h3 = (h3 + c) % 4294967296
        h4 = (h4 + d) % 4294967296
        h5 = (h5 + e) % 4294967296

    # Convert h-variables into hexadecimal, concatenate them, then return digest
    digest = [hex(h1)[2:], hex(h2)[2:], hex(h3)[2:], hex(h4)[2:], hex(h5)[2:]]
    for i in range(5):
        digest[i] = '0' * (8 - len(digest[i])) + digest[i]
    return ''.join(digest)


# 'A Test' -> 8f0c0855915633e4a7de19468b3874c8901df043
# print(encrypt('A Test') == '8f0c0855915633e4a7de19468b3874c8901df043')
