import secrets 

# Calculates a^m mod n using binary exponentiation, O(logm)
def bin_exp_mod(a: int, m: int, n: int) -> int:

    result = 1
    base = a % n # a^1 mod n

    while m > 0:
        if m % 2 == 1:
            result = (result * base) % n # Break down m by it's bits, if we see a one, multiply to result 
        base = (base * base) % n # Use mod properties to calculate the the next power of 2 by squaring the previous result
        m = m // 2 # get next bit
    
    return result

# decompose n - 1 into 2^s * d, where s is an integer and d is an odd integer
def decompose(n: int) -> tuple:
    s = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        s += 1
    return d, s


# impelentation of miller rabin test
def miller_rabin_Test(n: int, witness: int, d: int, s: int) -> bool: 
    if bin_exp_mod(witness, d, n) == 1: # First condition witness^d congruent to 1 mod n
        return True
    power_of_2 = 1
    for _ in range(s): # Check if witness^[(each power of two less than 2^s-1) * d] is congruent to -1 mod n
        if bin_exp_mod(witness, power_of_2 * d, n) == n-1:
            return True
        power_of_2 *= 2

    return False # If no statement is true, witness is a witness to the compositeness of n

# checks if n is prime, with a false positive rate of 4^(-num_witnesses), uses miller rabin primality test
def isPrime(n: int, num_witnesses = 12) -> bool: 

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
    low_bound = 2 ** (bits - 1)
    for _ in range(tries):
        num = secrets.randbits(bits)
        if num < low_bound:
            num += low_bound
        if num % 2 == 0:
            num += 1
        if isPrime(num, num_witnesses):
            return num
    