import string
from Encode import standard_encode
from Errors import InputError
import secrets
import math
import numpy as np
import math

class Hill:
    def __init__(self, key: list):
        if not isinstance(key, list):
            raise InputError("Matrix needs to be a square matrix. Usage: Hill(list[list] key)")
        
        self.__encryption_key = np.array(key)
        shape = self.__encryption_key.shape
        self.shape = len(key) # for later

        if len(shape) != 2 or shape[0] != shape[1]:
            raise InputError("Matrix needs to be a square matrix. Usage: Hill(list[list] key)")
        
        
        det = int(round(np.linalg.det(self.__encryption_key)))
        if math.gcd(26, det % 26) != 1:
            raise InputError("Invalid matrix, not invertible. det(key) must be invertible mod 26, i.e gcd(26, det(key)) = 1, in order to be a valid key.")
        
        e = pow(det % 26, -1, 26)
        self.__decryption_key = e * np.round(np.linalg.inv(self.__encryption_key) * det).astype(int)  % 26

        alphabet = string.ascii_uppercase
        self.letter_to_num = {char: i for i, char in enumerate(alphabet)}
        self.num_to_letter = {i: char for i, char in enumerate(alphabet)}

    def changeKey(self, newKey: list) -> None:
        self.__encryption_key = np.array(newKey)
        shape = self.__encryption_key.shape



        if len(shape) != 2 or shape[0] != shape[1]:
            raise InputError("Matrix needs to be a square matrix. Usage: Hill(list[list] key)")
        
        
        det = int(round(np.linalg.det(self.__encryption_key)))

        if math.gcd(26, det % 26) != 1:
            raise InputError("Invalid matrix, not invertible. det(key) must be invertible mod 26, i.e gcd(26, det(key)) = 1, in order to be a valid key.")
        
        e = pow(det % 26, -1, 26)
        self.__decryption_key = e * np.round(np.linalg.inv(self.__encryption_key) * det).astype(int)  % 26

    def encrypt(self, plaintext: str) -> str:
        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")
        
        plaintext = standard_encode(plaintext, padBound=self.shape)
        ciphertext = []

        for i in range(0, len(plaintext), self.shape):
            word_vec = np.array([self.letter_to_num[plaintext[n]] for n in range(i, i + self.shape)])
            result_vec = np.dot(self.__encryption_key, word_vec) % 26
            fin_vec = [self.num_to_letter[i] for i in result_vec]

            for char in fin_vec:
                ciphertext.append(char)

        return ''.join(ciphertext)
            
    def decrypt(self, ciphertext: str) -> str:
        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        if (len(ciphertext) % self.shape != 0):
            raise InputError("Ciphertext must be a string that can be split evenly by the key dimension (length multiple of key dimension). Proper Usage: obj.decrypt(string ciphertext)")

        plaintext = standard_encode(ciphertext, padBound=self.shape)
        plaintext = []

        for i in range(0, len(ciphertext), self.shape):
            word_vec = np.array([self.letter_to_num[ciphertext[n]] for n in range(i, i + self.shape)])
            result_vec = np.dot(self.__decryption_key, word_vec) % 26
            fin_vec = [self.num_to_letter[i] for i in result_vec]

            for char in fin_vec:
                plaintext.append(char)

        return ''.join(plaintext)
            
    @staticmethod
    def generate_key(dim: int) -> int:
        while True:
            potential_key = np.array([[secrets.randbelow(26) for j in range(dim)] for i in range(dim)])
            det = int(round(np.linalg.det(potential_key))) % 26
            if math.gcd(det, 26) == 1:
                return potential_key.tolist()
            




