from Errors import InputError
import secrets
import Primes


class DH():
    def __init__(self, public :list[int]):
        """
        Initializes a Diffie Helman character, either Alice or Bob

        @param: public - a list for the public parameters, which will be [g, p], where g is the generator, and p is the prime

        @return: none
        """

        if len(public) != 2:
            raise InputError("public needs to be a list of two numbers, [g, p], such that generator g that is a primitive root of p")
        
        if not isinstance(public[0], int) or not isinstance(public[1], int):
            raise InputError("public needs to be a list of two numbers, [g, p], such that generator g that is a primitive root of p")
        
        if not Primes.is_primitive_root(public[0], public[1]):
            raise InputError("g is not a primitive root of p")
        
        self._public_param = public
        self.__private_param = secrets.randbelow(public[1] - 1)




    def change_private_param(self) -> None:

        """
        Changes the secret number such that it is still between [0, p - 1)

        @param: none

        @return: none
        """

        self.__private_param = secrets.randbelow(self._public_param[1] - 1)
    



    def change_public_param(self, public :list[int]) -> None:
        """
        Changes the public parameters g and p to the new specified parameters in public, [g, p]

        @param: none

        @return: none
        """

        if len(public) != 2:
            raise InputError("public needs to be a list of two numbers, [g, p], such that generator g that is a primitive root of p")
        
        if not isinstance(public[0], int) or not isinstance(public[1], int):
            raise InputError("public needs to be a list of two numbers, [g, p], such that generator g that is a primitive root of p")
        
        if not Primes.is_primitive_root(public[0], public[1]):
            raise InputError("g is not a primitive root of p")
        
        self._public_param = public




    def public_param(self) -> list:
        """
        Returns the public parameters [g, p]

        @param: none

        @return: list[int] public, [g, p]
        """
        return self._public_param




    @staticmethod
    def generate_key(self, bits: int) -> list:
        """
        Generates a prime p of bit length bits, and finds the smallest possible generator g. Time intensive method, don't rely on this. 

        @param: bits - the length in bits of the prime p

        @return: list[int], [g, p]
        """
        prime = Primes.generate_prime(bits)
        g = Primes.find_primitive_root(prime)
        return [g, prime]
    



    def send_component(self) -> int:
        """
        Emits message to other participant for the key exchange

        @param: none

        @return: the integer is the message that should be received by the other participant to find the shared secret
        """
        g, p = self.public_param()
        return pow(g, self.__private_param, p)
    



    def get_secret(self, receive: int) -> int:
        """
        Calculates the shared secret based on the message received from other participant

        @param: receive - the integer received from the other participant

        @return: the integer is the shared secret

        """
        _, p = self.public_param()
        return pow(receive, self.__private_param, p)

