from math import gcd, log
from random import randint
from primality_tests import is_prime
from multiprocessing import Pool


# Number Theory
############################################################################################################################################################################################################################################################################################################

# Returns the modular inverse of a given mod n using the Euclidean algorithm
def mod_inverse(a, n):
    # Integer and modulus must be co-prime for an inverse to exist
    if gcd(a, n) != 1:
        return None
    
    # Variables used for computation
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, n

    # Compute the inverse
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    
    # Return the inverse of a mod n
    return u1 % n


# Key Generator
############################################################################################################################################################################################################################################################################################################

# Creates a dictionary containing the primes, modulus n, ϕ(n), and keys e, d.
# Supports multi-prime RSA
def generate_keys(bit_size, primes = 2):
    # A minimum of 2 primes are required
    if primes < 2:
        primes = 2

    # Identity values
    n = 1
    phi_n = 1

    # The key will be returned once it has been filled out
    key = {'primes': [], 'modulus': None, 'phi_n': None, 'public_key': None, 'private_key': None}
    
    # A minimum of 128 bits is required
    if bit_size < 128:
        min_n = pow(2, 127)
        max_n = pow(2, 128) - 1
    else:
        min_n = pow(2, bit_size - 1)
        max_n = pow(2, bit_size) - 1
    
    # Find primes
    for _ in range(primes):
        # Randomly generate a number that has the specified bit size
        p = randint(min_n, max_n)

        # Check if it's a unique prime. If not, generate another number
        while p in key['primes'] or not is_prime(p):
            p = randint(min_n, max_n)
        
        # Add the prime to the list and update n and phi_n
        key['primes'].append(p)
        n *= p
        phi_n *= (p - 1)
    
    # After the primes have been found, update the key
    key['modulus'] = n
    key['phi_n'] = phi_n
    
    # Generate the public and private keys
    inverseFound = False
    while not inverseFound:
        # Generate a random number e (possible public key)
        e = randint(65537, phi_n)
        if gcd(e, phi_n) == 1: # e must be co-prime to phi_n for an inverse to exist
            d = mod_inverse(e, phi_n) # Private key

            # To improve security, d should have a large number of digits
            if (log(d, 10) + 1) > (3 * (log(phi_n, 10) + 1) / 4):
                inverseFound = True
    
    # Add the public and private keys to the list
    key['public_key'] = e
    key['private_key'] = d
    
    # Return the keys
    return key


# String/Block Converter
############################################################################################################################################################################################################################################################################################################

# Uses a generator to convert a string into blocks of integers
def string_to_blocks(text, block_size):
    # Iterate through each chunk of text
    for block_start in range(0, len(text), block_size):
        block_int = 0
        
        # Convert each chunk to a number
        for power, char in enumerate(text[block_start : block_start + block_size]):
            block_int += ord(char) * (UNICODE_VAL ** power)
        
        # Yield the block (generator)
        yield block_int


# Uses a generator to convert blocks of integers into a string
def blocks_to_string(block_ints, block_size):
    # Iterate through each integer block
    for block_int in block_ints:
        block_message = []

        # Convert each block into a chunk of text
        for power in reversed(range(block_size)):
            char_index = block_int // (UNICODE_VAL ** power)

            # Extract character codes if they exist
            if char_index != 0:
                block_int %= (UNICODE_VAL ** power)
                block_message.append(chr(char_index))
        
        # Yield the text (generator)
        yield ''.join(reversed(block_message))


# Finds the maximum block size
def max_block_val(bit_size):
    return int(log(pow(2, bit_size - 1), UNICODE_VAL))


# Maximum number of characters in the Unicode table: 1114112
UNICODE_VAL = 128


# RSA Cryptosystem
############################################################################################################################################################################################################################################################################################################

# Encrypts a message using RSA
# NOTE: multi-processing is used to speed up calculations (maximum of 8 CPU cores)
def encrypt(message, e, n, block_size = 2):
    # Context manager
    with Pool(8) as p:
        # Generator feeds arguments into the pow() function in the next line
        args = ((block, e, n) for block in string_to_blocks(message, block_size))

        # Use multi-processing to encrypt the blocks, then concatenate and return them
        return '.'.join((f"{result}" for result in p.starmap(pow, args)))


# Decrypts a message using RSA
# NOTE: multi-processing is used to speed up calculations (maximum of 8 CPU cores)
def decrypt(block_message, d, n, block_size = 2):
    # Context manager
    with Pool(8) as p:
        # Generator feeds arguments into the pow() function in the next line
        args = ((int(block), d, n) for block in block_message.split('.'))

        # Use multi-processing to decrypt the blocks, then convert and return the message
        return ''.join(blocks_to_string((result for result in p.starmap(pow, args)), block_size))


# Testing
############################################################################################################################################################################################################################################################################################################

# Tests [n, e, d] using a specified number of iterations
def test_keys(key, iterations = 10):
    # Test the keys using different numbers
    for x in range(2, 2 + iterations):
        # If the number isn't the same after encryption and decryption, then return false
        if x != pow(pow(x, key['public_key'], key['modulus']), key['private_key'], key['modulus']):
            return False

    # Return true if the keys passed the tests
    return True 
