import secrets 


def bin_exp_mod(a: int, m: int, n: int) -> int:
    """

    Calculates a^m mod n

    @param: a - the base
    @param: m - the exponent
    @param: n - the modulus

    @return: the smallest positive number congruent to a^m mod n

    """
    result = 1
    base = a % n # a^1 mod n

    while m > 0:
        if m % 2 == 1:
            result = (result * base) % n # Break down m by it's bits, if we see a one, multiply to result 
        base = (base * base) % n # Use mod properties to calculate the the next power of 2 by squaring the previous result
        m = m // 2 # get next bit
    
    return result

def decompose(n: int) -> tuple:

    """

    decomposes integer n - 1 into (2^s) * d, where s is and integer and d is an odd integer

    @param: n - the number to be decomposed

    @return: (d, s), where n - 1 = (2^s) * d

    """

    s = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        s += 1
    return d, s


# impelentation of miller rabin test
def miller_rabin_Test(n: int, witness: int, d: int, s: int) -> bool: 

    """

    An implementation of the miller rabin test with a singular witness
    
    @param: n - the number for which is being checked for it's primality
    @param: witness - a potential witness for the primality of n
    @param: d - see decompose(n), the first number returned from this tuple
    @param: s - see decompose(n), the second number returned from this tuple

    @return: True if the witness is a witness to the primality of n, and False if the witness is a witness to the compositness of n

    """

    if bin_exp_mod(witness, d, n) == 1: # First condition witness^d congruent to 1 mod n
        return True
    power_of_2 = 1
    for _ in range(s): # Check if witness^[(each power of two less than 2^s-1) * d] is congruent to -1 mod n
        if bin_exp_mod(witness, power_of_2 * d, n) == n-1:
            return True
        power_of_2 *= 2

    return False # If no statement is true, witness is a witness to the compositeness of n

def isPrime(n: int, num_witnesses = 12) -> bool: 

    """

    A probablistic test to determine whether a number is prime, with a false positive rate of 4^(-num_witnesses)
    
    @param: n - the number for which is being checked for it's primality
    @param: num_witnesses - the number of witnesses to be chosen to check for the primality of n

    @return: True if n is prime, False if not. Has a very high chance of being correct.

    """

    # Base Cases
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    d, s = decompose(n)

    for _ in range(num_witnesses): # runs the miller rabin test num_witness amount of times
        curr_witness = secrets.randbelow(n - 4) + 2
        if not miller_rabin_Test(n, curr_witness, d, s):
            return False
        
    return True

    
def generate_prime(bits: int, num_witnesses = 12, tries = 10000) -> int:
    """

    Generates a prime number that is @param bits long, ie between 2^(bits - 1) and 2^(bits) - 1

    @param: bits - the desired bit length of the prime
    @param: num_witnesses - the number of desired witnesses to validate the primality of a candidate prime using the Miller Rabin Test
    @param: tries - the number of potential candidates generated

    @return: a number that is prime that has a bit length of @param bits

    """
    low_bound = 2 ** (bits - 1)
    for _ in range(tries):
        num = secrets.randbits(bits)
        if num < low_bound:
            num += low_bound
        if num % 2 == 0:
            num += 1
        if isPrime(num, num_witnesses):
            return num
    