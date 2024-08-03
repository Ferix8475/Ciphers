from Affine import Affine
from Caesar import Caesar
import DH
import ElGamal
import RSA
from Hill import Hill
from OTP import OTP
from Playfair import Playfair
from Sub import SimpleSubstitution
from Transposition import RectangularTransposition
from Vigenere import Vigenere
import string
import random
from sympy import factorint


def random_string(length: int) -> string:
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWYZ") for _ in range(length))


# Test the Classical Cryptosystems that are all encapsulated within a single class. 
def test_classical(runs = 200, subtests = 20, string_size = 1000):
    factor = random.choice(list(factorint(string_size).keys()))
    for _ in range(runs):
        keylen = random.randint(1, 26)
        affine_key = Affine.generate_key()
        ciphers = [Affine(affine_key[0], affine_key[1]), 
                   Caesar(Caesar.generate_key()), 
                   Hill(Hill.generate_key(2)), 
                   OTP(OTP.generate_key(string_size * 5)),
                   Playfair(Playfair.generate_key(keylen)), 
                   SimpleSubstitution(SimpleSubstitution.generate_key()), 
                   RectangularTransposition(RectangularTransposition.generate_key(factor)), 
                   Vigenere(Vigenere.generate_key(keylen))]
        for _ in range(subtests):
            test_string = random_string(string_size)
            playfair_test_string = test_string.replace('J', 'I')


            for cipher in ciphers:
                ciphertext = cipher.encrypt(test_string)
                plaintext = cipher.decrypt(ciphertext)

                #Playfair requires some extra work
                if type(cipher) == Playfair:
                    plaintext = plaintext.replace('X', '')
                    if playfair_test_string != plaintext:
                        raise ValueError(f'Failed on {test_string} with {cipher}, ciphertext = {ciphertext}, decrypted plaintext = {plaintext}')
                    continue

                if test_string != plaintext:
                    raise ValueError(f'Failed on {test_string} with {cipher}, ciphertext = {ciphertext}, decrypted plaintext = {plaintext}')
        print('Passed one subtest!!')
                
test_classical()
