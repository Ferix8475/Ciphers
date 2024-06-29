import string
from Encode import standard_encode
from Errors import InputError
import secrets
from collections import OrderedDict

class RectangularTransposition:

    def __init__(self, key: str):

        if not isinstance(key, str):
            raise InputError("Key must be a string. Proper Usage: RectangularTransposition(string key)")
        

        for char in key:
            if not char.isalpha():
                raise InputError("Key must be an alphabetic string. Proper Usage: RectangularTransposition(string key)")

        key = list(OrderedDict.fromkeys(standard_encode(key)))
        sortkey = sorted(key)
        index_map = {char: i for i, char in enumerate(key)}

        self.__encryption_key = [index_map[char] for char in sortkey]

        self.__decryption_key = [0] * len(self.__encryption_key)
        for index, value in enumerate(self.__encryption_key):
            self.__decryption_key[value] = index
        

        
       
    # Key must have only one instance of each of the 26 letters (Uppercase or Lowercase)
    def changeKey(self, newKey: str) -> None:

        if not isinstance(newKey, str):
            raise InputError("Key must be a string. Proper Usage: RectangularTransposition(string key)")
        

        for char in newKey:
            if not char.isalpha():
                raise InputError("Key must be an alphabetic string. Proper Usage: RectangularTransposition(string key)")

        newKey = list(OrderedDict.fromkeys(standard_encode(newKey)))
        newKey = sorted(newKey)
        index_map = {char: i for i, char in enumerate(newKey)}

        index_map = {char: i for i, char in enumerate(newKey)}
        
        self.__encryption_key = [index_map[char] for char in newKey]

        self.__decryption_key = [0] * len(self.__encryption_key)
        for index, value in enumerate(self.__encryption_key):
            self.__decryption_key[value] = index

        
       

    # Plaintext must be a string
    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")

        plaintext = standard_encode(plaintext, padBound = len(self.__encryption_key))

        keyLen = len(self.__encryption_key)
        ciphertext = []
        for x in range(0, len(plaintext), keyLen):
            ciphertext += [plaintext[x + self.__encryption_key[i]] for i in range(keyLen)]


        return ''.join(ciphertext)

    # Ciphertext must be a string with all upper case alphabetic characters with no spaces
    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")
            
        plaintext = standard_encode(ciphertext, padBound = len(self.__decryption_key))

        keyLen = len(self.__decryption_key)
        plaintext = []
        for x in range(0, len(ciphertext), keyLen):
            plaintext += [ciphertext[x + self.__decryption_key[i]] for i in range(keyLen)]


        return ''.join(plaintext)
    
    @staticmethod
    def generate_key(length : int) -> string:
       characters = string.ascii_uppercase
       return ''.join(secrets.choice(characters) for _ in range(length))

        
x = RectangularTransposition("GGUUAARRDD")
