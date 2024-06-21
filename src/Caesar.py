import string
from Encode import standard_encode
from Errors import InputError
import secrets

class Caesar:
    def __init__(self, shift):

        if not isinstance(shift, int):
            raise InputError("The Key/Shift must be an integer. Proper Usage: Caesar(int shift)")

        shift = shift % 26
        alphabet = string.ascii_uppercase
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        self.encryption_table = str.maketrans(alphabet, shifted_alphabet)
        self.decryption_table = str.maketrans(shifted_alphabet, alphabet)

    def changeKey(self, newShift: int) -> None:

        if not isinstance(newShift, int):
            raise InputError("The Key/Shift must be an integer. Proper Usage: obj.changeKey(int newShift)")

        newShift = newShift % 26
        alphabet = string.ascii_uppercase
        shifted_alphabet = alphabet[newShift:] + alphabet[:newShift]
        self.encryption_table = str.maketrans(alphabet, shifted_alphabet)
        self.decryption_table = str.maketrans(shifted_alphabet, alphabet)

    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")

        return standard_encode(plaintext).translate(self.encryption_table)

    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        for char in ciphertext:
            if not char.isupper():
                raise InputError("Ciphertext must strictly contain upper case letters. Proper Usage: obj.decrypt(string ciphertext)")


        return ciphertext.translate(self.decryption_table)
    
    @staticmethod
    def generate_key() -> int:
        return secrets.randbelow(26)