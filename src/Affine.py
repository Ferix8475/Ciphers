import string
from Encode import standard_encode
from Errors import InputError
import secrets
import math

class Affine:
    def __init__(self, a: int, b: int):

        a = a % 26
        b = b % 26

        if not isinstance(a, int) or not isinstance(b, int):
            raise InputError("The 'a' and 'b' values must be integers. Proper Usage: Affine(int a, int b)")

        if math.gcd(26, a) != 1:
            raise InputError("Invalid 'a' value. 'a' must be invertible mod 26, i.e gcd(26, a) = 1, in order to be a valid key.")

        num_to_alpha = {i: chr(65 + i) for i in range(26)}
        alphabet = string.ascii_uppercase
        shifted_alphabet = ""

        for n in range(26):
            shifted_alphabet += num_to_alpha[(a * n + b) % 26]

        self.__encryption_key = str.maketrans(alphabet, shifted_alphabet)
        self.__decryption_key = str.maketrans(shifted_alphabet, alphabet)

    def changeKey(self, new_a: int, new_b: int) -> None:

        new_a = new_a % 26
        new_b = new_b % 26

        if not isinstance(new_a, int) or not isinstance(new_b, int):
            raise InputError("The 'a' and 'b' values must be integers. Proper Usage: Affine(int new_a, int new_b)")

        if math.gcd(26, new_a) != 1:
            raise InputError("Invalid 'a' value. 'a' must be invertible mod 26, i.e gcd(26, a) = 1, in order to be a valid key.")

        num_to_alpha = {i: chr(65 + i) for i in range(26)}
        alphabet = string.ascii_uppercase
        shifted_alphabet = ""

        for n in range(26):
            shifted_alphabet += num_to_alpha[(new_a * n + new_b) % 26]

        self.__encryption_key = str.maketrans(alphabet, shifted_alphabet)
        self.__decryption_key = str.maketrans(shifted_alphabet, alphabet)

    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")

        return standard_encode(plaintext).translate(self.__encryption_key)

    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")

        return ciphertext.translate(self.__decryption_key)
    
    @staticmethod
    def generate_key() -> int:
        a = [1,3,5,7,9,11,15,17,19,21,23,25]
        return [secrets.choice(a), secrets.randbelow(26)]


