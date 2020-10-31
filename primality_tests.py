from math import sqrt
import numpy as np

# Primality Testing

# Returns a list of primes less than n using Sieve of Erathosthenes' algorithm
def sieve_of_erathosthenes(n):
    # List of integers from 1 to n-1 (assume all are prime for now)
    sieve = np.ones(n, dtype="bool")

    # Zero and one are not prime
    sieve[0] = False
    sieve[1] = False

    # Iterate the multiples of each integer, from 1 to sqrt(n), as composite
    for number in range(2, int(sqrt(n)) + 1):
        # If the integer is prime, flag its multiples as composite
        if sieve[number]:
            k = number * 2
            while k < n:
                sieve[k] = False
                k += number
    
    # Return the list of integers from 1 to n-1 that are still listed as prime
    return np.array([number for number in range(n) if sieve[number]])


# Determines if n is a prime by using the Miller-Rabin primality test
# Uses 100 different bases for testing
def miller_rabin(n):
    # Return true if n is 2 or 3
    if n == 2 or n == 3:
        return True

    # Return false if n is divisible by 2    
    if n % 2 == 0:
        return False
    
    m = n - 1
    t = 0

    while m % 2 == 0:
        m = m // 2
        t += 1
    
    # Try 100 different numbers to see if n is prime
    for number in range(2, 102):
        v = pow(number, m, n)

        if not v == 1 and not v == n - 1:
            i = 0

            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % n
                    
                    if v == 1:
                        return False
    return True


# Uses a probabilistic method of determining if a number is prime
def is_prime(n):
    # Integers less than 2 are not prime
    if n < 2:
        return False
    
    # Check the sieve list if n is prime or not
    for prime in SIEVE_LIST:
        if n == prime: 
            # n is in the list, so it's prime
            return True
        elif n % prime == 0:
            # n isn't in the list, but is a multiple of a number in the list, so it's composite
            return False
    
    # Try the Miller-Rabin primality last
    return miller_rabin(n)


# List of primes under 1,000,000
SIEVE_LIST = sieve_of_erathosthenes(1_000_000)