"""
John Montgomery 29/03/21 - NEA 2022
"""

class ArgumentError(BaseException):
    def __init__(self, message):
        super().__init__(message)
