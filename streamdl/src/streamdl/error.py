class StreamdlError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    
class InvalidURLError(StreamdlError):
    def __init__(self, *args):
        message = "The link is Invalid" + " ".join(args)
        super().__init__(message)
        
