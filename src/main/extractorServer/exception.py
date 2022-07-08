class ExtractorServerException(Exception):
    def __init__(self, message, error_code: int = 500, **kwargs):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.json_kwargs = kwargs
