# Department Settings
import json
class DepartmentSettings():
    def __init__(self):
        self.name = None
        self.chair = None
        self.start_time = None
        self.end_time = None

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
        f = open('department_settings.json', 'w')
        f.write(contents)


