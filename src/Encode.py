"""
Encoding method for most of the classical cryptosystems, adds padding if required
@param: plaintext - the plaintext to be encoded
        padBound - if padding needs to be added, the number for which the encoded plaintext needs to be divisible by
@return: The plaintext, stripped of nonalphabetic characters, with every character made upper case, and additional padding if needed
"""
def standard_encode(plaintext: str, padBound = 1) ->  str: 
    plaintext = ''.join(char.upper() for char in plaintext if char.isalpha())
    return plaintext + 'X' * (len(plaintext) % padBound)


