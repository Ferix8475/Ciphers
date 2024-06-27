import Encode
from Errors import InputError
import secrets
import math
import Primes
import base64


class RSA_key():
    def __init__(self, primes = [5, 5]):
        """
        Initializes the RSA_key object, creating the public and private keys

        @param: primes - A list of two integers that must be prime. These will be denoted as p and q, and used to generate n, d, and e

        @Attributes: self.__public_key - the public key, (n, e)
        @Attributes: self.__private_key - the private key, (n, d)
        @Attributes: self.size - the bit length of modulus n

        """
        if len(primes) != 2:
            raise InputError("p must be a list of two prime numbers")
        
        p, q = primes

        if not isinstance(p, int) or not isinstance(q, int):
            raise InputError("p must be a list of two prime numbers")
        
        if not Primes.isPrime(p) or not Primes.isPrime(q):
            raise InputError("p and q must be prime numbers")
        
        n = p * q
        phi_n = (p - 1) * (q - 1)


        while True:
            d = secrets.randbelow(phi_n - 1) + 1
            if math.gcd(d, phi_n) == 1:
                break
        
        e = pow(d, -1, phi_n)
        self.__public_key = (n, e)
        self.size = n.bit_length()
        self.__private_key = (n, d)
    



    def public_key(self):

        """
        Returns the public key, (n, e)
        """

        return self.__public_key
    



    def _private_key(self):

        """
        Returns the private key, (n, d)
        """

        return self.__private_key




    def load_public_key(self, filename):
        """

        Loads the encoded public key from the specified file (.pem)

        @param: filename - the file that the public key is on

        @return: none

        """
        with open(filename, 'r') as f:
            pem_data = f.read()

        pem_data = pem_data.strip()
        if not pem_data.startswith('-----BEGIN RSA PUBLIC KEY-----') or not pem_data.endswith('-----END RSA PUBLIC KEY-----'):
            raise InputError("Invalid RSA public key PEM format")

        # Extract base64 encoded data
        pem_data = pem_data.replace('-----BEGIN RSA PUBLIC KEY-----', '').replace('-----END RSA PUBLIC KEY-----', '').strip()
        der_bytes = base64.decodebytes(pem_data.encode('ascii'))

       
        key_bytes = der_bytes[1:]  # Skip ASN.1 header if present
        n_length = key_bytes[1]
        n = int.from_bytes(key_bytes[2:2 + n_length], 'big')
        e_length = key_bytes[2 + n_length + 1]
        e = int.from_bytes(key_bytes[2 + n_length + 2: 2 + n_length + 2 + e_length], 'big')

        self.__public_key = (n, e)




    def load_private_key(self, filename):
        """

        Loads the encoded private key from the specified file (.pem)

        @param: filename - the file that the private key is on

        @return: none

        """
        with open(filename, 'r') as f:
            pem_data = f.read()

        pem_data = pem_data.strip()
        if not pem_data.startswith('-----BEGIN RSA PRIVATE KEY-----') or not pem_data.endswith('-----END RSA PRIVATE KEY-----'):
            raise InputError("Invalid RSA private key PEM format")

        # Extract base64 encoded data
        pem_data = pem_data.replace('-----BEGIN RSA PRIVATE KEY-----', '').replace('-----END RSA PRIVATE KEY-----', '').strip()
        der_bytes = base64.decodebytes(pem_data.encode('ascii'))

        
        key_bytes = der_bytes[1:]  # Skip ASN.1 header if present
        n_length = key_bytes[1]
        n = int.from_bytes(key_bytes[2:2 + n_length], 'big')
        d_length = key_bytes[2 + n_length + 1]
        d = int.from_bytes(key_bytes[2 + n_length + 2: 2 + n_length + 2 + d_length], 'big')

        self.__private_key = (n, d)




    def public_key_tofile(self, filename):
        """

        Writes the encoded public key onto a file (.pem)

        @param: filename - the file to be written to

        @return: none

        """
        n, e = self.public_key()  
        pem_data = (
            f"-----BEGIN RSA PUBLIC KEY-----\n"
            f"{base64.encodebytes(self._der_encode_rsa_public_key(n, e)).decode('ascii')}"
            f"-----END RSA PUBLIC KEY-----\n"
        )
        with open(filename, 'w') as f:
            f.write(pem_data)




    def private_key_tofile(self, filename):

        """

        Writes the encoded public key onto a file (.pem)

        @param: filename - the file to be written to

        @return: none

        """

        n, d = self._private_key()  
        pem_data = (
            f"-----BEGIN RSA PRIVATE KEY-----\n"
            f"{base64.encodebytes(self._der_encode_rsa_private_key(n, d)).decode('ascii')}"
            f"-----END RSA PRIVATE KEY-----\n"
        )
        with open(filename, 'w') as f:
            f.write(pem_data)




    def _der_encode_rsa_public_key(self, n, e):
        """

        Encode the public key (n, e) using ASN.1 DER

        @param: n - the modulus of the RSA key
        @param: e - the public encryption key

        @return: the encoded public key

        """

        n_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        e_bytes = e.to_bytes((e.bit_length() + 7) // 8, 'big')

        n_length = len(n_bytes)
        e_length = len(e_bytes)

        der_encoded = (
            b'\x30' +  
            b'\x02' + bytes([n_length]) + n_bytes +  # Integer n
            b'\x02' + bytes([e_length]) + e_bytes   # Integer d
        )

        return der_encoded




    def _der_encode_rsa_private_key(self, n, d):
        """

        Encode the private key (n, d) using ASN.1 DER

        @param: n - the modulus of the RSA key
        @param: d - the private decryption key

        @return: The encoded private key

        """
        
        n_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        d_bytes = d.to_bytes((d.bit_length() + 7) // 8, 'big')

        n_length = len(n_bytes)
        d_length = len(d_bytes)

        der_encoded = (
            b'\x30' +  # Sequence tag
            b'\x02' + bytes([n_length]) + n_bytes +  # Integer n
            b'\x02' + bytes([d_length]) + d_bytes   # Integer d
        )

        return der_encoded
    



def generate_primes(size: int) -> list:
    """

    Generate two primes that have a product of @param size or size - 1 bits

    @param: size - the size of the product of the two primes (which will become the modulus n)

    @return: the two primes as a list, [p, q]

    """
    prime_size = size // 2
    p = Primes.generate_prime(prime_size)
    q = Primes.generate_prime(prime_size)
    return [p, q]




def encrypt(plaintext: str, key: RSA_key) -> int:
    """

    Encrypts the given plaintext using the key provided. Encodes plaintext using PKCS #1 1.5, then applies the encryption exponent

    @param: plaintext - the plaintext to be encrypted, in the form of a string
    @param: key - the key to be used, which will provide the public key, (n, e)

    @return: The ciphertext in the form of an integer

    """

    padded_plaintext = Encode.pkcs1_v15_pad(plaintext, key.size)
    n, e = key.public_key()
    return pow(padded_plaintext, e, n)




def decrypt(ciphertext: int, key: RSA_key) -> str:

    """

    Decrypts the given plaintext using the key provided. Applies the decryption exponent, then decodes into the plaintext 

    @param: ciphertext - the ciphertext to be decrypted, in the form of an int
    @param: key - the key to be used, which will provide the private key, (n, d)

    @return: The plaintext in the form of a string

    """

    n, d = key._private_key()
    padded_plaintext = pow(ciphertext, d, n)
    return Encode.pkcs1_v15_decode(padded_plaintext)
    