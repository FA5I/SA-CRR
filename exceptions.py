class NotImplementedError(Exception):
    """Exception for not implemented parts of the specification """

    def __init__(self, message):
        self.message = message
