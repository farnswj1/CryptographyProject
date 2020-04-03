from math import gcd, log
from random import randint
from primality_tests import is_prime

# Number Theory
############################################################################################################################################################################################################################################################################################################

# Returns the modular inverse of a given mod n using the Euclidean algorithm
def mod_inverse(a, n):
    if gcd(a, n) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, n
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % n


# Key Generator
############################################################################################################################################################################################################################################################################################################

#Creates a list containing the primes, modulus n, ϕ(n), and keys e, d: [[factors of n], n, ϕ(n), e, d]
#Supports multi-prime RSA
def generate_keys(bit_size, primes = 2):
    if primes < 2:
        primes = 2

    n = 1
    phi_n = 1
    key = {'primes': [], 'modulus': None, 'phi_n': None, 'public_key': None, 'private_key': None}
    
    if bit_size <= 32:
        min_n = 2147483648
        max_n = 4294967295
    else:
        min_n = pow(2, bit_size - 1)
        max_n = pow(2, bit_size) - 1
    
    for i in range(primes):
        p = randint(min_n, max_n)
        while p in key['primes'] or not is_prime(p):
            p = randint(min_n, max_n)
        key['primes'].append(p)
        n *= p
        phi_n *= (p - 1)
    
    key['modulus'] = n
    key['phi_n'] = phi_n
    
    while True:
        e = randint(65537, phi_n)
        if gcd(e, phi_n) == 1:
            d = mod_inverse(e, phi_n)
            if d != None and (log(d, 10) + 1) > (3 * (log(phi_n, 10) + 1) / 4):
                break
    
    key['public_key'] = e
    key['private_key'] = d
    return key


# String/Block Converter
############################################################################################################################################################################################################################################################################################################

# Converts a string into blocks of integers
def string_to_blocks(text, block_size):
    block_ints = []
    for block_start in range(0, len(text), block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(text))):
            block_int += ord(text[i]) * (UNICODE_VAL ** (i % block_size))
        block_ints.append(block_int)
    return block_ints


# Converts blocks of integers into a string
def blocks_to_string(block_ints, block_size):
     text = []
     for block_int in block_ints:
         block_message = []
         for i in range(block_size - 1, -1, -1):
             char_index = block_int // (UNICODE_VAL ** i)
             if char_index != 0:
                 block_int %= (UNICODE_VAL ** i)
                 block_message.insert(0, chr(char_index))
         text.extend(block_message)
     return ''.join(text)


# Finds the maximum block size
def max_block_val(bit_size):
    return int(log(pow(2, bit_size - 1), UNICODE_VAL))


# Maximum number of characters in the Unicode table: 1114112
UNICODE_VAL = 128


# RSA Cryptosystem
############################################################################################################################################################################################################################################################################################################

# Encrypts a message using RSA
def encrypt(message, e, n, block_size = 2):
    block_message = string_to_blocks(message, block_size)
    for i in range(len(block_message)):
        block_message[i] = str(pow(block_message[i], e, n))
    return '.'.join(block_message)


# Decrypts a message using RSA
def decrypt(block_message, d, n, block_size = 2):
    block_message = [int(i) for i in block_message.split('.')]
    for i in range(len(block_message)):
        block_message[i] = pow(block_message[i], d, n)
    return blocks_to_string(block_message, block_size)


# Testing
############################################################################################################################################################################################################################################################################################################

# Tests [n, e, d] using a specified number of iterations
def test_keys(key, iterations = 10):
    for x in range(2, 2 + iterations):
        if x != pow(pow(x, key['public_key'], key['modulus']), key['private_key'], key['modulus']):
            return False
    return True
