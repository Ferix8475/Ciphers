import string
from Encode import standard_encode
from Errors import InputError
import secrets

class SimpleSubstitution:

    # Key must have only one instance of each of the 26 letters (Uppercase or Lowercase)
    def __init__(self, key: str):

        if not isinstance(key, str):
            raise InputError("Key must be a string. Proper Usage: SimpleSubstitution(string key)")
        
        if len(key) != 26:
            raise InputError("Key must have one of each of the upper case letters")

        alphabetSet = set(string.ascii_uppercase)
        if set(key) != alphabetSet:
            raise InputError("Key must have one upper case instance of each of the letters")

        #key = standard_encode(key)
        alphabet = string.ascii_uppercase
        self.encryption_table = str.maketrans(alphabet, key)
        self.decryption_table = str.maketrans(key, alphabet)

    # Key must have only one instance of each of the 26 letters (Uppercase or Lowercase)
    def changeKey(self, newKey: str) -> None:

        if not isinstance(newKey, str):
            raise InputError("Key must be a string. Proper Usage: obj.changeKey(string key)")
        
        if len(newKey) != 26:
            raise InputError("Key must have one of each of the upper case letters")

        alphabetSet = set(string.ascii_uppercase)
        if set(newKey) != alphabetSet:
            raise InputError("Key must have one upper case instance of each of the letters")
        
        alphabet = string.ascii_uppercase
        self.encryption_table = str.maketrans(alphabet, newKey)
        self.decryption_table = str.maketrans(newKey, alphabet)

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
    
