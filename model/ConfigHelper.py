import configparser

class ConfigHelper:

    def __init__(self, filepath):
        self.filepath = filepath    
        self.config = configparser.ConfigParser()
        with open('config.ini', 'r', encoding='utf-8') as f:
            self.config.read_file(f)

    def refreshSchedule(self, scheduleList):
        # ConfigParser expects a mapping of string->string for a section.
        # Build a dict where each schedule becomes a key with an empty string value.
        newSchedule = {}
        index = 1
        description = {}  # Section name in the config file
        for schedule in scheduleList:
            # ensure the key is a string (ConfigParser requires string keys)
            newSchedule[schedule] = ""

        self.config['Schedule'] = newSchedule
        with open(self.filepath, 'w', encoding="utf-8") as configfile:
            self.config.write(configfile)
