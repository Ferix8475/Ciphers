from Errors import InputError
import secrets

def standard_encode(plaintext: str, padBound = 0) ->  str: 
    """

    Encoding method for most of the classical cryptosystems, adds padding if required.
    
    @param: plaintext - the plaintext to be encoded.
    @param: padBound - if padding needs to be added, the number for which the encoded plaintext needs to be divisible by.

    @return: The plaintext, stripped of nonalphabetic characters, with every character made upper case, and additional padding if needed.

    """


    plaintext = ''.join(char.upper() for char in plaintext if char.isalpha())
    if not padBound or len(plaintext) % padBound == 0:
        return plaintext
    else: 
        return plaintext + 'Z' * (padBound - (len(plaintext) % padBound))

def pkcs1_v15_pad(plaintext: str, key_size: int) -> bytes:
    """

    Padding method for RSA using PKCS #1 v1.5.

    @param: plaintext - the plaintext to be encoded, as a string.
    @param: padBound - the size of the key in bits.

    @return: An integer representation of the plaintext, padded using PKCS #1 1.5.

    """

    plaintext_bytes = plaintext.encode('ascii')
    key_size_bytes = (key_size ) // 8 # bits to bytes
    max_plaintext_length = key_size_bytes - 11  # 11 bytes overhead for security
    
    if len(plaintext_bytes) > max_plaintext_length:
        raise InputError("Plaintext length exceeds maximum allowable length for RSA encryption for this specific key of size " + str(key_size))
    
    padding_length = key_size_bytes - len(plaintext) - 3 # 3 bytes for labels
    padding = b'\x00\x02' + bytes([secrets.randbelow(254) + 1 for _ in range(padding_length)]) + b'\x00'
    padded_plaintext = padding + plaintext_bytes
    padded_plaintext_int = int.from_bytes(padded_plaintext, byteorder='big')
    return padded_plaintext_int

def pkcs1_v15_decode(padded_plaintext_int: int) -> str:
    """

    Decoding method for RSA using PKCS #1 v1.5.

    @param: padded_plaintext_int - the Encoded plaintext with PKCS #1 1.5 padding.

    @return: A string representation of the original plaintext.

    """
    padded_plaintext_bytes = padded_plaintext_int.to_bytes(((padded_plaintext_int.bit_length() + 15) // 8), 'big') # add extra padding so that you see x00
    
    if padded_plaintext_bytes[0:2] != b'\x00\x02':
        raise InputError("Decoded text does not follow PKCS #1 v1.5 Encoding, missing initial bytes 0x00 and 0x02")
    
    # Find the separator byte 0x00
    try:
        separator_index = padded_plaintext_bytes.index(b'\x00', 2)
    except ValueError:
        raise ValueError("Decoded text does not follow PKCS #1 v1.5 Encoding, missing separator byte 0x00")
    
    # Extract and return the plaintext without padding
    plaintext_bytes = padded_plaintext_bytes[separator_index + 1:]
    plaintext = plaintext_bytes.decode('ascii')
    return plaintext

