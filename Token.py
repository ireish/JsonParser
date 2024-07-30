class Token:
    def __init__(self, token_type, start, end, value=None):
        self.token_type = token_type
        self.start = start
        self.end = end
        self.value = value

    def __str__(self):
        return f"Token({self.token_type}, {self.value})"

    
