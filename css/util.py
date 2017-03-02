from django.core.exceptions import ValidationError
import re

# Department Settings
import json
class DepartmentSettings():
    def __init__(self):
        self.name = None
        self.chair = None
        self.start_time = "00:00"
        self.end_time = "00:00"

    @classmethod
    def load_settings(cls):
        obj = cls()
        contents = json.loads(open('department_settings.json', 'r').read())
        obj.name = contents['name']
        obj.chair = contents['chair']
        obj.start_time = contents['start_time']
        obj.end_time = contents['end_time']
        return obj

    # Write new department settings to file
    def save_settings(self):
        contents = json.dumps(self.__dict__, indent=4)
        with open("department_settings.json", 'w') as dept_settings_file:
            dept_settings_file.write(contents)

    def new_settings(self, name=None, chair=None, start_time=None, end_time=None):
        if name is not None:
            if len(name) > 32:
                raise ValidationError("Name is too long")
            else:
                self.name = name
        if chair is not None:
            if len(chair) > 32: 
                raise ValidationError("Chair name is too long")
            else:
                self.chair = chair
        if start_time is not None:
            if re.match(r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', start_time) is None:
                raise ValidationError("Invalid start time")
            else:
                self.start_time = start_time
        if end_time is not None:
            if re.match(r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', end_time) is None:
                raise ValidationError("Invalid end time")
            else:
                self.end_time = end_time
        self.save_settings()
        

# Custom FileContent error. Used when parsing inavlid data within file
class FileParserError(Exception):
    """ Raise for problems parsing input files """
    pass


