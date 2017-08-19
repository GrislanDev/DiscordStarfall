"""
Module helps to deal with file IO regarding .json files.
"""

import json

class File:

    def __init__(self, path):
        """ Stores and retrieves data from a .json file.

        Attributes:
            path = The <str> used to retrive the file
            save = An object with .json data from the file
        """
        
        self.path = path
        self.save = None
        
        self.load_save()

    def __str__(self):
        r = ""
        r += "Path: " + self.path + "\n"
        return r

    def load_save(self):
        """ Ensures that info written to file is saved in self.save."""
        with open(self.path,'r') as f:
            self.save = json.loads(f.read())
        return self.save

    def write_save(self):
        """ Write info from self.save to self.file."""
        with open(self.path, 'w') as f:
            f.truncate()
            f.write(json.dumps(self.save))
        return self.save
        
    def empty(self):
        """ Clears file."""
        with open(self.path, 'w') as f:
            f.truncate()

        self.load_save()

