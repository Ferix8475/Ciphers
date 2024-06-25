from Errors import InputError
import secrets

def standard_encode(plaintext: str, padBound = 0) ->  str: 
    """
    Encoding method for most of the classical cryptosystems, adds padding if required
    @param: plaintext - the plaintext to be encoded
            padBound - if padding needs to be added, the number for which the encoded plaintext needs to be divisible by
    @return: The plaintext, stripped of nonalphabetic characters, with every character made upper case, and additional padding if needed
    """
    plaintext = ''.join(char.upper() for char in plaintext if char.isalpha())
    if not padBound or len(plaintext) % padBound == 0:
        return plaintext
    else: 
        return plaintext + 'Z' * (padBound - (len(plaintext) % padBound))

class RSA_encoder():
    def __init__(key_length: int):
        NotImplemented

    def pkcs1_v15_pad(plaintext: str, key_size: int) -> bytes:
        key_size_bytes = key_size // 8 # bits to bytes
        max_plaintext_length = key_size_bytes - 11  # 11 bytes overhead for PKCS#1 v1.5 padding
        
        if len(plaintext) > max_plaintext_length:
            raise InputError("Plaintext length exceeds maximum allowable length for RSA encryption for this specific key of size " + key_size)
        
        padding_length = key_size_bytes - len(plaintext) - 3 # 3 bytes for labels
        padding = b'\x00\x02' + bytes([secrets.randbelow(254) + 1 for _ in range(padding_length)]) + b'\x00'
        padded_plaintext = padding + plaintext
        return padded_plaintext

    def pkcs1_v15_decode(ciphertext: int):

        ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')

        if ciphertext_bytes[0:2] != b'\x00\x02':
            raise InputError("Invalid Encoded ciphertext")
        
        # Find the separator byte 0x00
        try:
            separator_index = ciphertext_bytes.index(b'\x00', 2)
        except ValueError:
            raise ValueError("Invalid PKCS#1 v1.5 padding")
        
        # Extract and return the plaintext without padding
        plaintext = ciphertext_bytes[separator_index + 1:]
        return plaintext

