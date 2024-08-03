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

test_p = 10320218115367600288400551792891159809760797028267953990358141197047679350550387485255857487116786974035314217183369639241205784634603955112324260653788107
test_q = 13257097284859458686720086336676073705930751305914696876923749886308569400552934872514588389992051427044302345172591985408347033882535512548033299953497447
test_g = 2

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
                
def test_RSA_EG(runs = 200, string_size=50):

    keys = [RSA.RSA_key([test_p, test_q]),
            ElGamal.ElGamal_Key(p=test_p, g=test_g)]
    
    for _ in range(runs):
        test_string = random_string(string_size)

        ciphertext = RSA.encrypt(test_string, keys[0])
        plaintext = RSA.decrypt(ciphertext, keys[0])

        if test_string != plaintext:
            raise ValueError(f'Failed on {test_string} with RSA, ciphertext = {ciphertext}, decrypted plaintext = {plaintext}')

        ciphertext = ElGamal.encrypt(test_string, keys[1])
        plaintext = ElGamal.decrypt(ciphertext, keys[1])

        if test_string != plaintext:
            raise ValueError(f'Failed on {test_string} with RSA, ciphertext = {ciphertext}, decrypted plaintext = {plaintext}')

        print('Passed run!!!')


def test_DH(runs = 200): # Keep string_size fixed for this test, there isn't much tolerance because of prime bit sizes

    alice = DH.DH(g=test_g, p = test_p)
    bob = DH.DH(g=test_g, p = test_p)
    
    for _ in range(runs):
        
        bob_comp = bob.send_component()
        alice_comp = alice.send_component()

        alice_secret = alice.get_secret(bob_comp)
        bob_secret = bob.get_secret(alice_comp)

        if alice_secret != bob_secret:
            raise ValueError(f'Failed!')

        alice.change_private_param()
        bob.change_private_param()

        print('Passed Run!!!')

test_DH()
test_RSA_EG()
test_classical()
