from math import sqrt

#Primality Testing

#Returns a list of primes less than n using Sieve of Erathosthenes' algorithm
def prime_sieve(n):
    sieve = [True] * n
    sieve[0] = False
    sieve[1] = False
    for i in range(2, int(sqrt(n)) + 1):
        if sieve[i] == False:
            continue
        k = i * 2
        while k < n:
            sieve[k] = False
            k += i
    primes = []
    for i in range(n):
        if sieve[i] == True:
            primes.append(i)
    return primes 


#List of primes under 1000000
sieve_list = prime_sieve(1000000)


#Determines if n is a prime by using the Miller-Rabin primality test
#Uses 100 different bases for testing
def miller_rabin(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    m = n - 1
    t = 0
    while m % 2 == 0:
        m = m // 2
        t += 1
    for trials in range(2, 102):
        v = pow(trials, m, n)
        if v == 1 or v == n - 1:
            continue
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


#Uses a probabilistic method of determining if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for prime in sieve_list:
        if n == prime:
            return True
        elif n % prime == 0:
            return False
    return miller_rabin(n)
