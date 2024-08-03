import string
from Encode import standard_encode
from Errors import InputError
import secrets

class OTP:
    def __init__(self, key: str):
        
        self.key_error = "The Key must be an alphabetic string.\n It is suggested to use the generate_key method to create a randomized key for One-Time Pad, which can be called using OTP.generate_key(int keyLength).\n Proper Usage: OTP(string key)"

        if not isinstance(key, str):
            raise InputError(self.key_error)
        
        for char in key:
            if not char.isalpha():
                raise InputError(self.key_error)

        self.__key = standard_encode(key)


    def changeKey(self, newKey: str) -> None:

        if not isinstance(newKey, str):
            raise InputError(self.key_error)

        for char in newKey:
            if not char.isalpha():
                raise InputError(self.key_error)
            
        self.__key = standard_encode(newKey)

    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")
        
        if len(plaintext) > len(self.__key):
            print(plaintext)
            print(self.__key)
            raise InputError("Plaintext must be shorter than the key. Proper Usage: obj.encrypt(string plaintext)")
        
        plaintext = standard_encode(plaintext)

        ciphertext = []

        for x in range(len(plaintext)):
            toAdd = ((ord(plaintext[x]) + ord(self.__key[x])) % 26) + 65 # 65 is ASCII of A
            ciphertext.append(chr(toAdd))

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        if len(ciphertext) > len(self.__key):
            raise InputError("Ciphertext must be shorter than the key. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")

        plaintext = []

        for x in range(len(ciphertext)):
            toAdd = ((ord(ciphertext[x]) - ord(self.__key[x]) + 26) % 26) + 65 # 65 is ASCII of A
            plaintext.append(chr(toAdd))

        return ''.join(plaintext)
    
    @staticmethod
    def generate_key(length : int) -> string:
       characters = string.ascii_uppercase
       return ''.join(secrets.choice(characters) for _ in range(length))



