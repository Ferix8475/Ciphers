from Errors import InputError
import secrets
import Primes
import Encode
import base64

class ElGamal_Key():
    def __init__(self, p: int, g: int):
        """
        Initializes an ElGamal object based on generator g of prime p, creating a random public and private key

        @param: g - the generator component of the public key
        @param: p - the prime number componenent of the public key

        @return: none
        """

      
        if not isinstance(g, int) or not isinstance(p, int):
            raise InputError("g and p need to be integers. Usage: obj = ElGamal_Key(int p, int g)")
        
        if not Primes.is_primitive_root(g, p):
            raise InputError("g is not a primitive root of p. Usage: obj = ElGamal_Key(int p, int g)")
        

        self.__private_key = secrets.randbelow(p)

        h = pow(g, self.__private_key, p)
        self._public_key = (p, g, h)




    def public_key(self) -> tuple:
        """
        Returns the public key (p, g, h)

        @param: none

        @return: tuple[int], (p, g, h)
        """
        return self._public_key




    def _private_key(self) -> int:
        """
        Returns the private key, x

        @param: none

        @return: int, private key x
        """
        return self.__private_key


    
    @staticmethod
    def load_public_key(filename):
        """

        Loads the encoded public key from the specified file (.pem)

        @param: filename - the file that the public key is on

        @return: none

        """
        with open(filename, 'r') as f:
            pem_data = f.read()

        pem_data = pem_data.strip()
        if not pem_data.startswith('-----BEGIN ELGAMAL PUBLIC KEY-----') or not pem_data.endswith('-----END ELGAMAL PUBLIC KEY-----'):
            raise InputError("Invalid ELGAMAL public key PEM format")

        # Extract base64 encoded data
        pem_data = pem_data.replace('-----BEGIN ELGAMAL PUBLIC KEY-----', '').replace('-----END ELGAMAL PUBLIC KEY-----', '').strip()
        der_bytes = base64.decodebytes(pem_data.encode('ascii'))

       
        key_bytes = der_bytes[1:]  
        p_length = key_bytes[1]
        p = int.from_bytes(key_bytes[2:2 + p_length], 'big')
        g_length = key_bytes[2 + p_length + 1]
        g = int.from_bytes(key_bytes[2 + p_length + 2: 2 + p_length + 2 + g_length], 'big')
        h_length = key_bytes[2 + p_length + 2 + g_length + 1]
        h = int.from_bytes(key_bytes[2 + p_length + 2 + g_length + 2:2 + p_length + 2 + g_length + 2 + h_length], 'big')

        return p, g, h



    @staticmethod
    def load_private_key(filename):
        """

        Loads the encoded private key from the specified file (.pem)

        @param: filename - the file that the private key is on

        @return: none

        """
        with open(filename, 'r') as f:
            pem_data = f.read()

        pem_data = pem_data.strip()
        if not pem_data.startswith('-----BEGIN ELGAMAL PRIVATE KEY-----') or not pem_data.endswith('-----END ELGAMAL PRIVATE KEY-----'):
            raise InputError("Invalid ElGamal private key PEM format")

        # Extract base64 encoded data
        pem_data = pem_data.replace('-----BEGIN ELGAMAL PRIVATE KEY-----', '').replace('-----END RSA PRIVATE KEY-----', '').strip()
        der_bytes = base64.decodebytes(pem_data.encode('ascii'))

        key_bytes = der_bytes[1:]  
        x_length = key_bytes[1]
        x = int.from_bytes(key_bytes[2:2 + x_length], 'big')
       
      
        
        

        return x




    def public_key_tofile(self, filename):
        """

        Writes the encoded public key onto a file (.pem)

        @param: filename - the file to be written to

        @return: none

        """
        p, g, h= self.public_key()  
        pem_data = (
            f"-----BEGIN ELGAMAL PUBLIC KEY-----\n"
            f"{base64.encodebytes(self._der_encode_eg_public_key(p, g, h)).decode('ascii')}"
            f"-----END ELGAMAL PUBLIC KEY-----\n"
        )
        with open(filename, 'w') as f:
            f.write(pem_data)




    def private_key_tofile(self, filename):

        """

        Writes the encoded public key onto a file (.pem)

        @param: filename - the file to be written to

        @return: none

        """

        x = self._private_key()  
        pem_data = (
            f"-----BEGIN ELGAMAL PRIVATE KEY-----\n"
            f"{base64.encodebytes(self._der_encode_eg_private_key(x)).decode('ascii')}"
            f"-----END ELGAMAL PRIVATE KEY-----\n"
        )
        with open(filename, 'w') as f:
            f.write(pem_data)




    def _der_encode_eg_public_key(self, p, g, h):
        """

        Encode the public key (p, g, h) using ASN.1 DER

        @param: p - the modulus of the key
        @param: g - the generator component of the public key
        @param: h - the 3rd part of the public key

        @return: the encoded public key

        """

        p_bytes = p.to_bytes((p.bit_length() + 7) // 8, 'big')
        g_bytes = g.to_bytes((g.bit_length() + 7) // 8, 'big')
        h_bytes = h.to_bytes((h.bit_length() + 7) // 8, 'big')

        p_length = len(p_bytes)
        g_length = len(g_bytes)
        h_length = len(h_bytes)

        der_encoded = (
            b'\x30' +  
            b'\x02' + bytes([p_length]) + p_bytes +  
            b'\x02' + bytes([g_length]) + g_bytes + 
            b'\x02' + bytes([h_length]) + h_bytes
        )

        return der_encoded




    def _der_encode_eg_private_key(self, x):
        """

        Encode the private key x using ASN.1 DER

        @param: x - the private exponent key 

        @return: The encoded private key

        """
        
    
        x_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
        x_length = len(x_bytes)

        der_encoded = (
            b'\x30' +  
            b'\x02' + bytes([x_length]) + x_bytes 
        )

        return der_encoded

def generate_key_seed(bits: int) -> tuple:
    """
    Generates a prime p of bit length bits, and finds the smallest possible generator g. Time intensive method, don't rely on this. 

    @param: bits - the length in bits of the prime p

    @return: tuple[int], (p, g)
    """

    prime = Primes.generate_prime(bits)
    g = Primes.find_primitive_root(prime)
    return prime, g
    
def encrypt(plaintext: str, key: ElGamal_Key) -> int:

    """

    Encrypts the plaintext with the given key using ElGamal 

    @param: plaintext - the plaintext as a string
    @param: key - The ElGamal key object

    
    @return: The ciphertext as pair (c1, c2)

    """

    if not isinstance(plaintext, str):
        raise InputError("Input plaintext must be a string. Usage: ElGamal.encrypt(str plaintext, ElGamal_Key key)")

    if not isinstance(key, ElGamal_Key):
        raise InputError("Input key must be an ElGamal_Key. Usage: ElGamal.encrypt(str plaintext, ElGamal_Key key)")
    
    p, g, h = key.public_key()
    eph_key = secrets.randbelow(p)

    key_size = p.bit_length()
    encoded_plaintext = Encode.pkcs1_v15_pad(plaintext, key_size)

    s = pow(h, eph_key, p)
    c1 = pow(g, eph_key, p)
    c2 = (encoded_plaintext * s) % p

    return (c1, c2)

def decrypt(ciphertext: tuple[int], key: ElGamal_Key) -> str:

    """

    Decrypts the ciphertext (c1, c2) with the given key using ElGamal 

    @param: ciphertext - the ciphertext (c1, c2)
    @param: key - The ElGamal key object

    
    @return: The plaintext as a string

    """
    if not isinstance(ciphertext, tuple):
        raise InputError("Ciphertext must be a tuple of two integers. Usage: ElGamal.encrypt(str plaintext, ElGamal_Key key)")

    if not isinstance(key, ElGamal_Key):
        raise InputError("Input key must be an ElGamal_Key. Usage: ElGamal.encrypt(str plaintext, ElGamal_Key key)")


    p, _, _ = key.public_key()
    priv_key = key._private_key()
    c1, c2 = ciphertext

    if not isinstance(c1, int) or not isinstance(c2, int):
        raise InputError("Ciphertext must be a tuple of two integers. Usage: ElGamal.encrypt(str plaintext, ElGamal_Key key)")

    s = pow(c1, priv_key, p)
    inv_s = pow(s, -1, p)
    plaintext_encoded = (c2 * inv_s) % p

    return Encode.pkcs1_v15_decode(plaintext_encoded)

