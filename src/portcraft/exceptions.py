
class MissingTokenError(Exception):
    def __init__(self):
        super().__init__("Token is required for this repo")
