'''
Justin Farnsworth
Cryptography Project

'''

from time import sleep
import rsa
import helper
import sha1
import sha224
import sha256
import sha384
import sha512
import sha512_224
import sha512_256


# Main program function
def main():
    print("Justin Farnsworth\nCryptography Project - RSA\n")
    print("This program will encrypt and decrypt a message using RSA.")
    print("The user can experiment with various parameters, such as bitsize and blocksize.")
    print(
        """Notable features of this program include, but are not limited to:
            •Primality testing (Sieve of Erathosthenes, Miller-Rabin)    
            •2-prime & Multi-prime RSA   
            •Hash functions"""
    )
    print("WARNING: Hashing will only be allowed on 8-bit character strings!")
    sleep(3)

    # Main loop
    while True:
        # User inputs bitsize
        while True:
            try:
                bits = int(input("Select the desired number of bits for your primes (128 minimum): "))
                if bits == -1:
                    print("Terminating program...")
                    sleep(0.5)
                    return
                elif bits < 128:
                    print("We need at least 128 bits.")
                else:
                    break
            except:
                print("This is not an integer.")
        
        # Calculate max blocksize
        max_blocks = rsa.max_block_val(bits)
        
        # User inputs number of primes
        while True:
            try:
                primes = int(input("Select the desired number of primes (2 minimum): "))
                if primes < 2:
                    print("We need at least 2 primes.")
                else:
                    break
            except:
                print("This is not an integer.")
        
        # User inputs blocksize
        while True:
            try:
                user_block_size = int(input(f"Select the desired blocksize (1 - {max_blocks}): "))
                if not 1 <= user_block_size <= max_blocks:
                    print("This is not within the required range!")
                else:
                    break
            except:
                print("This is not an integer.")
        
        # Key/modulus generation and testing
        print("Generating modulus and keys for RSA...")
        keys_and_mod = rsa.generate_keys(bits, primes)
        
        print("Testing keys and modulus...")
        while not rsa.test_keys(keys_and_mod):
            print("Test failed! Generating new modulus and keys for RSA...")
            keys_and_mod = rsa.generate_keys(bits, primes)
            print("Testing keys and modulus...")
        
        # Display public key, private key, and modulus
        print(f"Public key: {keys_and_mod['public_key']}")
        print(f"Private key: {keys_and_mod['private_key']}")
        print(f"Modulus: {keys_and_mod['modulus']}")
        print(f"ϕ: {keys_and_mod['phi_n']}")
        sleep(2)
        
        # Display prime (optional)
        while True:
            try:
                factor_option = str(input("Would you like to see the primes that generate the modulus? (Y/N): ")).upper()
                if factor_option in ['Y', "YES"]:
                    for i in range(len(keys_and_mod['primes'])):
                        print(f"P{i + 1}: {keys_and_mod['primes'][i]}")
                    sleep(2)
                    break
                elif factor_option in ['N', "NO"]:
                    break
                print("Invalid option!")
            except:
                print("Invalid option!")
        
        # User inputs plaintext
        while True:
            try:
                plaintext = str(input("Insert your plaintext message: "))
                if plaintext:
                    break
                print("Invalid option!")
            except:
                print("This message will not work. Try another message.")
        
        # Encrypting message
        print("Encrypting message...")
        ciphertext = rsa.encrypt(plaintext, keys_and_mod['public_key'], keys_and_mod['modulus'], user_block_size)
        print(ciphertext)
        sleep(2)
        
        # Decrypting message (optional)
        while True:
            try:
                decrypt_option = str(input("Would you like to decrypt this message? (Y/N): ")).upper()
                if decrypt_option in ['Y', 'N', "YES", "NO"]:
                    break
                print("Invalid option!")
            except:
                print("Invalid option!")
        
        if decrypt_option in ['Y', "YES"]:
            print("Decrypting message...")
            decrypted_message = rsa.decrypt(ciphertext, keys_and_mod['private_key'], keys_and_mod['modulus'], user_block_size)
            print(decrypted_message)
            sleep(2)
            if decrypted_message == plaintext:
                print("Your message was fully recovered!")
            else:
                print("YOUR MESSAGE WAS CORRUPTED!")
            sleep(2)
        
        # Encrypt message via hashing
        # Only applies to 8-bit character strings
        flag_for_hash = helper.is_8bit(plaintext)
        hash_option = ''
        while flag_for_hash:
            try:
                hash_option = str(input("Would you like to encrypt your original message via hashing? (Y/N): ")).upper()
                if hash_option in ['Y', 'N', "YES", "NO"]:
                    break
                print("Invalid option!")
            except:
                print("Invalid option!")
        
        if hash_option in ['Y', "YES"]:
            print("Encypting...")
            print(f"SHA-1:       {sha1.encrypt(plaintext)}")
            print(f"SHA-224:     {sha224.encrypt(plaintext)}")
            print(f"SHA-512/224: {sha512_224.encrypt(plaintext)}")
            print(f"SHA-256:     {sha256.encrypt(plaintext)}")
            print(f"SHA-512/256: {sha512_256.encrypt(plaintext)}")
            print(f"SHA-384:     {sha384.encrypt(plaintext)}")
            print(f"SHA-512:     {sha512.encrypt(plaintext)}")
            sleep(2)
        
        # Resets program (optional)
        while True:
            try:
                program_option = str(input("Would you like to restart this program? (Y/N): ")).upper()
                if program_option in ['Y', 'N', "YES", "NO"]:
                    break
                print("Invalid option!")
            except:
                print("Invalid option!")
        
        if program_option in ['N', "NO"]:
            print("Terminating program...")
            sleep(1)
            return
    
        print("Restarting program...")
        sleep(1) 


# Executes program
if __name__ == '__main__':
    main()
