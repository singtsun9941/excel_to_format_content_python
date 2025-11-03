import configparser

class Config:

    def __init__(self, filepath):
        self.filepath = filepath  
        self.config = configparser.ConfigParser()
        self.config.read(self.filepath)

    def getData(self):
        return self.config
