

class Label:
    def __init__(
            self,
            name,
            filename_format=None):
        self.name = name
        self.filename_format = filename_format or str()
