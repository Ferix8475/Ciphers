import string
from Encode import standard_encode
from Errors import InputError
import secrets

class Vigenere:
    def __init__(self, key: str):

        if not isinstance(key, str):
            raise InputError("The Key must be an alphabetic string. Proper Usage: Vigenere(string key)")
        
        for char in key:
            if not char.isalpha():
                 raise InputError("The Key must be an alphabetic string. Proper Usage: Vigenere(string key)")

        self.__key = standard_encode(key)


    def changeKey(self, newKey: str) -> None:

        if not isinstance(newKey, str):
            raise InputError("The Key must be an string. Proper Usage: Vigenere (string key)")

        for char in newKey:
            if not char.isalpha():
                 raise InputError("The Key must be an alphabetic string. Proper Usage: Vigenere(string key)")

        self.__key = standard_encode(newKey)

    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")
        
        plaintext = standard_encode(plaintext)
        keyLength = len(self.__key)

        ciphertext = []

        for x in range(len(plaintext)):
            toAdd = ((ord(plaintext[x]) + ord(self.__key[x % keyLength])) % 26) + 65 # 65 is ASCII of A
            ciphertext.append(chr(toAdd))

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")

        keyLength = len(self.__key)

        plaintext = []

        for x in range(len(ciphertext)):
            toAdd = ((ord(ciphertext[x]) - ord(self.__key[x % keyLength]) + 26) % 26) + 65 # 65 is ASCII of A
            plaintext.append(chr(toAdd))

        return ''.join(plaintext)
    
    @staticmethod
    def generate_key(length : int) -> string:
       characters = string.ascii_uppercase
       return ''.join(secrets.choice(characters) for _ in range(length))


