import string
from Encode import standard_encode
from Errors import InputError
import secrets
from collections import OrderedDict

class Playfair:

    def __init__(self, key: str):

        if not isinstance(key, str):
            raise InputError("Key must be a string. Proper Usage: Playfair(string key)")
        

        for char in key:
            if not char.isalpha():
                raise InputError("Key must be an alphabetic string. Proper Usage: Playfair(string key)")
        
        alphabet_minus_J = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.__cord_to_letter = list(OrderedDict.fromkeys(standard_encode(key).replace('J', 'I') + alphabet_minus_J))

        self.__letter_to_cord = {x: (i // 5, i % 5) for i, x in enumerate(self.__cord_to_letter)}
        
        
        
       
    def changeKey(self, newKey: str) -> None:

        if not isinstance(newKey, str):
            raise InputError("Key must be a string. Proper Usage: RectangularTransposition(string key)")
        

        for char in newKey:
            if not char.isalpha():
                raise InputError("Key must be an alphabetic string. Proper Usage: RectangularTransposition(string key)")

        alphabet_minus_J = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.__cord_to_letter = list(OrderedDict.fromkeys(standard_encode(newKey).replace('J', 'I') + alphabet_minus_J))

        self.__letter_to_cord = {x: (i // 5, i % 5) for i, x in enumerate(self.__cord_to_letter)}
        
    # Plaintext must be a string
    def encrypt(self, plaintext: str) -> str:

        if not isinstance(plaintext, str):
            raise InputError("Plaintext must be a string. Proper Usage: obj.encrypt(string plaintext)")

        # encode text for encryption
        plaintext = standard_encode(plaintext).replace("J", "I")
        plaintext_pairs = []
        i = 0
        while i < len(plaintext):
            if i == len(plaintext) - 1:
                plaintext_pairs.append((plaintext[i], "X"))
                i += 1
            elif plaintext[i] == plaintext[i + 1]:
                plaintext_pairs.append((plaintext[i], "X"))
                i += 1
            else:
                plaintext_pairs.append((plaintext[i], plaintext[i + 1]))
                i += 2
        
        ciphertext = []

        for pair in plaintext_pairs:
            new_pair = self.__transform(pair)
            ciphertext.append(new_pair[0])
            ciphertext.append(new_pair[1])


        return ''.join(ciphertext)

    # Ciphertext must be a string with all upper case alphabetic characters with no spaces
    def decrypt(self, ciphertext: str) -> str:

        if not isinstance(ciphertext, str):
            raise InputError("Ciphertext must be a string. Proper Usage: obj.decrypt(string ciphertext)")
        
        if (len(ciphertext) % 2 == 1):
            raise InputError("Ciphertext must be a string that can be split pairwise (length multiple of 2). Proper Usage: obj.decrypt(string ciphertext)")

        for char in ciphertext:
            if not char.isupper() or char == "J":
                raise InputError("Ciphertext must strictly contain upper case letters, excluding J. Proper Usage: obj.decrypt(string ciphertext)")
            
        

        # We expect that the string can already be split pairwise at this point
        
        plaintext = []
        i = 0

        while i < len(ciphertext):

            if ciphertext[i] == ciphertext[i + 1]:
                raise InputError("Pairs must be two different letters. Encountered pair: " + (ciphertext[i], ciphertext[i + 1]))
            
            pair = (ciphertext[i], ciphertext[i + 1])
            new_pair = self.__transform(pair, encrypt=False)

            plaintext.append(new_pair[0])
            plaintext.append(new_pair[1])

            i += 2

       
        return ''.join(plaintext)
    

    def __transform(self, letters :tuple, encrypt = True):

        offset = 1 if encrypt else -1

        first_letter_coord, second_letter_coord = self.__letter_to_cord[letters[0]], self.__letter_to_cord[letters[1]]

        if (first_letter_coord[0] == second_letter_coord[0]):
            new_first = (first_letter_coord[0], (first_letter_coord[1] + offset) % 5)
            new_second = (second_letter_coord[0], (second_letter_coord[1] + offset) % 5)
        elif (first_letter_coord[1] == second_letter_coord[1]):
            new_first = ((first_letter_coord[0] + offset) % 5, first_letter_coord[1])
            new_second = ((second_letter_coord[0] + offset) % 5, second_letter_coord[1])
        else:
            new_first = (first_letter_coord[0], second_letter_coord[1])
            new_second = (second_letter_coord[0], first_letter_coord[1])


        return (self.__cord_to_letter[new_first[0] * 5 + new_first[1]], self.__cord_to_letter[new_second[0] * 5 + new_second[1]])

        

    @staticmethod
    def generate_key(length : int) -> string:
       characters = string.ascii_uppercase
       return ''.join(secrets.choice(characters) for _ in range(length))

