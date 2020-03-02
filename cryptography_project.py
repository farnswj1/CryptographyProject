'''
Justin Farnsworth
Cryptography Project

'''

from time import sleep
import rsa, helper, sha1, sha224, sha256, sha384, sha512, sha512_224, sha512_256


def print_program_info():
    print('Justin Farnsworth\nCryptography Project - RSA\n')
    print('This program will encrypt and decrypt a message using RSA.')
    print('The user can experiment with various parameters, such as bitsize and blocksize.')
    print('Notable features of this program include, but are not limited to:\n    •Primality testing (Sieve of Erathosthenes, Miller-Rabin)\n    •2-prime & Multi-prime RSA\n    •Hash functions')
    print('WARNING: Hashing will only be allowed on 8-bit character strings!')
    sleep(3)
    

#Main program function
def main():
    while True:
        #User inputs bitsize
        while True:
            try:
                bits = int(input('Select the desired number of bits for your primes (64 minimum): '))
                if bits == -1:
                    print('Terminating program...')
                    sleep(0.5)
                    return
                elif bits < 64:
                    print('We need at least 64 bits.')
                else:
                    break
            except:
                print('This is not an integer.')
        
        #Calculate max blocksize
        max_blocks = rsa.max_block_val(bits)
        
        #User inputs number of primes
        while True:
            try:
                primes = int(input('Select the desired number of primes (2 minimum): '))
                if primes < 2:
                    print('We need at least 2 primes.')
                else:
                    break
            except:
                print('This is not an integer.')
        
        #User inputs blocksize
        while True:
            try:
                user_block_size = int(input('Select the desired blocksize (1 - ' + str(max_blocks) + '): '))
                if not 1 <= user_block_size <= max_blocks:
                    print('This is not within the required range!')
                else:
                    break
            except:
                print('This is not an integer.')
        
        #Key/modulus generation and testing
        print('Generating modulus and keys for RSA...')
        keys_and_mod = rsa.generate_keys(bits, primes)
        
        print('Testing keys and modulus...')
        while not rsa.test_keys(keys_and_mod):
            print('Test failed! Generating new modulus and keys for RSA...')
            keys_and_mod = rsa.generate_keys(bits, primes)
            print('Testing keys and modulus...')
        
        #Display public key, private key, and modulus
        print('Public key: ' + str(keys_and_mod[3]))
        print('Private key: ' + str(keys_and_mod[4]))
        print('Modulus: ' + str(keys_and_mod[1]))
        print('ϕ: ' + str(keys_and_mod[2]))
        sleep(2)
        
        #Display prime (optional)
        while True:
            try:
                factor_option = str(input('Would you like to see the primes that generate the modulus? (Y/N): ')).upper()
                if factor_option in ['Y', 'YES']:
                    for i in range(len(keys_and_mod[0])):
                        print('P' + str(i + 1) + ": " + str(keys_and_mod[0][i]))
                    sleep(2)
                    break
                elif factor_option in ['N', 'NO']:
                    break
                print('Invalid option!')
            except:
                print('Invalid option!')
        
        #User inputs plaintext
        while True:
            try:
                plaintext = str(input('Insert your plaintext message: '))
                break
            except:
                print('This message will not work. Try another message.')
        
        #Encrypting message
        print('Encrypting message...')
        ciphertext = rsa.encrypt(plaintext, keys_and_mod[3], keys_and_mod[1], user_block_size)
        print(ciphertext)
        sleep(2)
        
        #Decrypting message (optional)
        while True:
            try:
                decrypt_option = str(input('Would you like to decrypt this message? (Y/N): ')).upper()
                if decrypt_option in ['Y', 'N', 'YES', 'NO']:
                    break
                print('Invalid option!')
            except:
                print('Invalid option!')
        
        if decrypt_option in ['Y', 'YES']:
            print('Decrypting message...')
            decrypted_message = rsa.decrypt(ciphertext, keys_and_mod[4], keys_and_mod[1], user_block_size)
            print(decrypted_message)
            sleep(2)
            if decrypted_message == plaintext:
                print('Your message was fully recovered!')
            else:
                print('YOUR MESSAGE WAS CORRUPTED!')
            sleep(2)
        
        #Encrypt message via hashing
        #Only applies to 8-bit character strings
        flag_for_hash = helper.is_8bit(plaintext)
        hash_option = ''
        while flag_for_hash:
            try:
                hash_option = str(input('Would you like to encrypt your original message via hashing? (Y/N): ')).upper()
                if hash_option in ['Y', 'N', 'YES', 'NO']:
                    break
                print('Invalid option!')
            except:
                print('Invalid option!')
        
        if hash_option in ['Y', 'YES']:
            print('Encypting...')
            print('SHA-1:       ' + sha1.encrypt(plaintext))
            print('SHA-224:     ' + sha224.encrypt(plaintext))
            print('SHA-512/224: ' + sha512_224.encrypt(plaintext))
            print('SHA-256:     ' + sha256.encrypt(plaintext))
            print('SHA-512/256: ' + sha512_256.encrypt(plaintext))
            print('SHA-384:     ' + sha384.encrypt(plaintext))
            print('SHA-512:     ' + sha512.encrypt(plaintext))
            sleep(2)
        
        #Resets program (optional)
        while True:
            try:
                program_option = str(input('Would you like to restart this program? (Y/N): ')).upper()
                if program_option in ['Y', 'N', 'YES', 'NO']:
                    break
                print('Invalid option!')
            except:
                print('Invalid option!')
        
        if program_option in ['N', 'NO']:
            print('Terminating program...')
            sleep(1)
            return
    
        print('Restarting program...')
        sleep(1) 


#Executes program
if __name__ == '__main__':
    print_program_info()
    main()


#References
'''
[1]  Al Sweigart, Cracking Codes with Python: An Introduction to Building and Breaking Ciphers, No Starch Press, San Francisco, CA, 2017
[2]  Wade Trappe and Lawrence C. Washington, Introduction to Cryptography with Coding Theory, 2nd Edition, Pearson Education, Upper Saddle River, NJ, 2006
[3]  https://www.geeksforgeeks.org/rotate-bits-of-an-integer/
[4]  https://en.wikipedia.org/wiki/SHA-1
[5]  https://en.wikipedia.org/wiki/SHA-2
[6]  Secure Hash Standard, National Institute of Standards and Technology, Gathersburg, MD, 2015
     http://dx.doi.org/10.6028/NIST.FIPS.180-4
[7]  http://www.abrahamlincolnonline.org/lincoln/speeches/gettysburg.htm
[8]  http://www.awon.org/dc3/
[9]  https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movie_Quotes
[10] https://www.goodreads.com/work/quotes/10446115-rocky-balboa
'''
