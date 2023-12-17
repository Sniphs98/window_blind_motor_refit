from logger import *
import json
import os

json_data = '''
{
    "SSID": "",
    "PASS": "",
    "STATIC_IP": "",
    "maxSteps": 13520,
    "openProcent": 0
}
'''

class Configurator:
    def __init__(self, logger):
        self.logger = logger
        self.data = json.loads(json_data)
        if not self.config_file_exist():
            logger.log("config file dont exist")
            self.create_json()       
        self.load_json()
        
    def create_json(self):
        try:
            self.logger.log_with_out_print("Try creatring config file")
            file = open ("config.json", "w")
            json.dump(self.data, file)
            file.close()  
            self.logger.log_with_out_print("config file created!")
        except Exception as e:
            self.logger.log("ERROR: IN CREATE_FILE BY Configurator")
            self.logger.log(str(e))
            
    def load_json(self):
        file = open("config.json", "r")
        self.data = json.load(file)
        file.close()
            
    def get_value(self, key):
        return self.data[key]
    
    def set_value(self, key, value):
        self.data[key] = value
        self.create_json()
        
    def config_file_exist(self):
        dir_iterator = os.ilistdir("./")
        for val in dir_iterator:
            if val[0] == "config.json":
                return True
        return False
    

