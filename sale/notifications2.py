#this file extends from the main notification class that we wrote
class Notification():
    def __init__(self, **kwargs):
        self.init_keys = kwargs.keys()
        self.init_values = kwargs.values()
        self.data = kwargs
        
    def set_notitfication_type_1(self):
        for key in self.init_keys:
            print self.data[key] 