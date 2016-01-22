# this file extends from the main notification class that we wrote
class Notification():
    ''' This class is for Main Notifications that are used in the app '''
    def __str__(self):
        return 'UserNotification'

    def __init__(self, **kwargs):
        self.init_keys = kwargs.keys()
        self.init_values = kwargs.values()
        self.data = kwargs

    def set_notitfication_type_1(self):
        for key in self.init_keys:
            print self.data[key]

    def set_notification_type_2(self):
        return self.data
