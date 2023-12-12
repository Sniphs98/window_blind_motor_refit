import json
from logger import *


class Configurator:
    def __init__(self, logger):
        self.logger = logger
    def create_file(self):
        try:
            self.logger.log("Try creatring config file")
            self.file = open ("config.json", "w")
            self.file.close()  
            self.logger.log("config file created!")
        except Exception as e:
            self.logger.log(str(e))