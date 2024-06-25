import string
import Encode
from Errors import InputError
import secrets
import math
import numpy as np
import math
import Primes


class RSA_key():
    def __init__(self, primes: list[int]):

        if len(primes) != 2:
            raise InputError("p must be a list of two prime numbers")
        
        p = primes[0]
        q = primes[1]

        if not isinstance(p, int) or not isinstance(p, int):
            raise InputError("p must be a list of two prime numbers")
        
        if not Primes.isPrime(p) or not Primes.isPrime(q):
            raise InputError("p and q must be prime numbers")
        
        n = p * q
        phi_n = (p - 1) * (q - 1)


        while True:
            self.__d = secrets.randbelow(phi_n - 1) + 1
            if math.gcd(self.__d, phi_n) == 1:
                break
        
        e = pow(self.__d, -1, phi_n)
        self.public_key = (n, e)
        self.size = n.bit_length

    
    def public_key(self):
        return self.public_key

def generate_primes(size: int) -> list:
    prime_size = size // 2
    p = Primes.generate_prime(prime_size)
    q = Primes.generate_prime(prime_size)
    print("done")
    return [p, q]

def encrypt(plaintext: str, key: RSA_key) -> int:
    NotImplemented

def decrypt(ciphertext: int, key: RSA_key) -> str:
    NotImplemented

x = RSA_key(generate_primes(256))
print(x.public_key)