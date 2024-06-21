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

        key = list(OrderedDict.fromkeys(key))
        key = [sorted(key).index(x) for x in key]
        
       
    # Key must have only one instance of each of the 26 letters (Uppercase or Lowercase)
    def changeKey(self, newKey: str) -> None:
        NotImplemented
       

    # Plaintext must be a string
    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")
        
        return standard_encode(plaintext).translate(self.encryption_table)

    # Ciphertext must be a string with all upper case alphabetic characters with no spaces
    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")
            
        return ciphertext.translate(self.decryption_table)
    
    @staticmethod
    def generate_key() -> str:
        key = list(string.ascii_uppercase)
        secrets.SystemRandom().shuffle(key)
        return ''.join(key)

        
    
