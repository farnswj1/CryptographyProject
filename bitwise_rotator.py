# Bitwise Rotator Module
# Note that the functions perform a circular rotation

# Rotates bits to the left d times
# Use for 32-bit integers only
def rotate_left_32bit(n, d): 
    return ((n << d) | (n >> (32 - d)) & 0xFFFFFFFF) % 4294967296


# Rotates bits to the right d times
# Use for 32-bit integers only
def rotate_right_32bit(n, d):
    return ((n >> d) | (n << (32 - d)) & 0xFFFFFFFF) % 4294967296


# Rotates bits to the left d times
# Use for 64-bit integers only
def rotate_left_64bit(n, d):
    return ((n << d) | (n >> (64 - d)) & 0xffffffffffffffff) % 18446744073709551616


# Rotates bits to the right d times
# Use for 64-bit integers only
def rotate_right_64bit(n, d): 
    return ((n >> d) | (n << (64 - d)) & 0xffffffffffffffff) % 18446744073709551616
