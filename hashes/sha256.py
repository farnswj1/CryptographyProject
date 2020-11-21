from .hash_pre_processor import convert_32bit
from .bitwise_rotator import rotate_right_32bit

# The 'Secure Hash Algorithm 256' cryptographic hash function
# Converts a string of 8-bit characters into a 64-hexadecimal value
def encrypt(string):
    # Pre-processing converts input string into a bit array
    string = convert_32bit(string)
    
    # Variables
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    v = (0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
         0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
         0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
         0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
         0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
         0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
         0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
         0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
         0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2)
    
    # Processing
    # Partition and build bit array into lists of eighty 32-bit binary strings
    for i in range(0, len(string), 512):
        bit_list = [int(string[i+j : i+j+32], 2) for j in range(0, 512, 32)]
            
        for k in range(16, 64):
            temp_A = rotate_right_32bit(bit_list[k - 15], 7) ^ rotate_right_32bit(bit_list[k - 15], 18) ^ bit_list[k - 15] >> 3
            temp_B = rotate_right_32bit(bit_list[k - 2], 17) ^ rotate_right_32bit(bit_list[k - 2], 19) ^ bit_list[k - 2] >> 10
            bit_list.append((bit_list[k - 16] + temp_A + bit_list[k - 7] + temp_B) % 4294967296)
        
        # Hash values
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        
        # Hashing loop
        for j in range(64):
            s = rotate_right_32bit(e, 6) ^ rotate_right_32bit(e, 11) ^ rotate_right_32bit(e, 25)
            t = (e & f) ^ ((~e & 0xffffffff) & g)
            temp_A = (h + s + t + v[j] + bit_list[j]) % 4294967296
            s = rotate_right_32bit(a, 2) ^ rotate_right_32bit(a, 13) ^ rotate_right_32bit(a, 22)
            t = (a & b) ^ (a & c) ^ (b & c)
            temp_B = (s + t) % 4294967296
            
            h = g
            g = f
            f = e
            e = (d + temp_A) % 4294967296
            d = c
            c = b
            b = a
            a = (temp_A + temp_B) % 4294967296

        h0 = (h0 + a) % 4294967296
        h1 = (h1 + b) % 4294967296
        h2 = (h2 + c) % 4294967296
        h3 = (h3 + d) % 4294967296
        h4 = (h4 + e) % 4294967296
        h5 = (h5 + f) % 4294967296
        h6 = (h6 + g) % 4294967296
        h7 = (h7 + h) % 4294967296

    # Convert h-variables into hexadecimal, concatenate them, then return digest
    return ''.join([hex(hvar)[2:].zfill(8) for hvar in (h0, h1, h2, h3, h4, h5, h6, h7)])


# 'A Test' -> 3445f19bb7bb8de4bdad54ec2871b1ca5a761de0115f6f741e298e4cc8f633ee
if __name__ == "__main__":
    print(encrypt('A Test') == '3445f19bb7bb8de4bdad54ec2871b1ca5a761de0115f6f741e298e4cc8f633ee')
