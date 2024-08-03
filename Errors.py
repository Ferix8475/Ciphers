class InputError(Exception):
    """
    A basic exception, I just like the word InputError 
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    