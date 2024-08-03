# Cipher Collection

A collection of various cryptographic algorithms in Python.

## Table of Contents

- [Description](#description)
- [Ciphers Included](#ciphers-included)
- [Installation](#installation)
- [Usage](#usage)

## Description

This project is a collection of various cryptographic algorithms implemented in Python. It includes classic ciphers like the Caesar cipher, modern cryptographic algorithms like RSA, and other encryption techniques. Each cipher is implemented in its own Python file, making it easy to explore and understand each algorithm independently.

## Ciphers/Protocols Included

- **Caesar Cipher** (`Caesar.py`): A simple substitution cipher where each letter in the plaintext is shifted a certain number of places down or up the alphabet.

- **Affine Cipher** (`Affine.py`): A substitution cipher that uses a mathematical formula involving multiplication and addition to shift each letter in the plaintext.

- **Simple Substitution**(`Sub.py`): A cipher that replaces each letter in the plaintext with a unique corresponding letter from a fixed substitution alphabet.

- **Playfair Cipher**(`Playfair.py`): A digraph substitution cipher that encrypts pairs of letters using a 5x5 grid of letters arranged according to a keyword.

- **Hill Cipher** (`Hill.py`): A polygraphic substitution cipher that uses linear algebra, specifically matrix multiplication, to encrypt blocks of text.

- **Rectangular Transposition Cipher** (`Transposition.py`): A method of encryption by rearranging the positions of the letters in the plaintext according to a certain system or pattern.

- **Vigenère Cipher** (`Vigenere.py`): A polyalphabetic substitution cipher that uses a keyword to shift letters, with the shift value depending on the corresponding letter in the keyword.

- **One Time Pad**(`OTP.py`): A theoretically unbreakable cipher that uses a single-use pre-shared key the same length as the message to encrypt the plaintext using the Vigenère.

- **Diffie-Hellman Key Exchange** (`DH.py`): A protocol for securely exchanging cryptographic keys over a public channel, allowing two parties to generate a shared secret key.

- **RSA Encryption** (`RSA.py`): A public-key cryptosystem that uses two keys (a public key and a private key) for secure data transmission, based on the mathematical properties of large prime numbers.

- **ElGamal**(`ElGamal.py`): A public-key cryptosystem based on the Diffie-Hellman key exchange, using asymmetric encryption for secure communication.

## Installation

### Prerequisites

- Python 3.x
- numpy
- sympy

### Installation Steps

To get a local copy up and running, follow these steps.

1. Clone the repository:
    ```sh
    git clone https://github.com/Ferix8475/Ciphers.git
    ```
2. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```
## Usage

To get started with the project, you can clone the repository and import the necessary modules into your Python scripts. Each module contains a class(es) that implements a specific cipher, which can be instantiated and used to encrypt or decrypt messages. You must import the these classes into your files properly in order to use the ciphers. Note that all of the Ciphers ignore non alphabetic characters (including spaces), so encrypting, then decrypting with the same key and cipher may not necessarily return the original plaintext. 

### Classical Ciphers

All of the classical ciphers are straightforward to use. For example, to use the Caesar Cipher:

```python
from Caesar import Caesar

cipher_obj = Caesar(6)
plaintext = "Today I Want To Go To The Beach But It's Raining"

ciphertext = cipher_obj.encrypt(plaintext)
decrypted_plaintext = cipher_obj.decrypt(ciphertext)
print(ciphertext, decrypted_plaintext)

cipher_obj.changeKey(20) # Change the Caesar Shift/Key
ciphertext = cipher_obj.encrypt(plaintext)
decrypted_plaintext = cipher_obj.decrypt(ciphertext)
print(ciphertext, decrypted_plaintext)

cipher_obj.changeKey(Caesar.generate_key()) # Generates a Random Key
ciphertext = cipher_obj.encrypt(plaintext)
decrypted_plaintext = cipher_obj.decrypt(ciphertext)
print(ciphertext, decrypted_plaintext)
```

Each of the Classical Ciphers (Affine, Caesar, Hill, Playfair, Substitution, Transposition, Vigenère, and One-Time-Pad) will all have these same methods (`encrypt(), decrypt(), generate_key(), changeKey(newKey)`), though some ciphers' `generate_key()` method require an argument. 


### RSA and ElGamal

For RSA and ElGamal, it is a little more complicated. You must first create an `RSA_Key` or `ElGamal_Key` object, for which you must provide two primes for an `RSA_Key` and a prime p and generator g for an `ElGamal_Key` object. These two key classes support saving and loading both the public and private components of the key. Then, to encrypt or decrypt plaintext, you simply call the methods directly from the files. 

```python
import RSA
import ElGamal

RSAKey = RSA.RSA_key(RSA.generate_primes(1024)) # Generates two primes who's product is 1024 bits
EGKey = ElGamal_Key(p, g) # Assume p and g are valid numbers

# Storing and Fetching keys from files
RSAKey.public_key_tofile('rsa_public.pem')
RSAKey.private_key_tofile('rsa_private.pem')

EGKey.public_key_tofile('eg_public.pem')
EGKey.private_key_tofile('eg_private.pem')

RSAKey.load_public_key('rsa_public.pem')
RSAKey.load_private_key('rsa_private.pem')

EGKey.load_public_key('eg_public.pem')
EGKey.load_private_key('eg_private.pem')

# Encrypting and Decrypting Text

plaintext = "Today I Slept"

ciphertext_rsa = RSA.encrypt(plaintext, RSAKey)
ciphertext_eg = ElGamal.encrypt(plaintext, EGKey)

decrypted_plaintext_rsa = RSA.decrypt(ciphertext_rsa, RSAKey)
decrypted_plaintext_eg = ElGamal.decrypt(ciphertext_eg, EGKey)
print(ciphertext_rsa, ciphertext_eg, decrypted_plaintext_rsa, decrypted_plaintext_eg)
```
### Diffie Helman Key Exchange

The DH Key Exchange requires creating two different DH objects created from the same prime p and generator g. DH objects support changing the public and private parameters (the second is automatically done when doing the first, and changing private parameters is always recommended after sharing a secret). To illustrate: 

```python
from DH import DH

g, p = DH.generate_key(2048) # Generate a random generator g and prime p 
alice = DH(g, p)
bob = DH(g, p)

# Perform the Exchange
bob_comp = bob.send_component()
alice_comp = alice.send_component()

# Calculate the Shared Secret
alice_secret = alice.get_secret(bob_comp)
bob_secret = bob.get_secret(alice_comp)

print(alice_secret == bob_secret) # Should print True

# Change private parameters after an exchange
alice.change_private_param()
bob.change_private_param()
```

## License

Distributed under the MIT License. See `LICENSE` for more information.