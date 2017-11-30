""" Creating and sending notification """
import time
import json
from scansell.settings import DEBUG

# Emoji constants
BOOK_EMOJI = b'\xF0\x9F\x93\x95'
SALE_EMOJI = b'\xF0\x9F\x99\x8C'

class Notification(object):
    """ Singleton class to create and send messages """
    def __init__(self, user):
        if user is None:
            raise Exception("user object required")
        self.user = user
    
    def build_notification_string(self, *args, **kwargs):
        """ Send args and kwargs to this method
            Returns a readable string for a notification
        """
        if len(args) < 1 or len(kwargs) <1:
            raise Exception("arguments required")
        
        display_string = list()

        # Add emoji to notification string to enchance readability
        try:
            # emoji _type is one of the pre-defined constants in the class
            emoji_type = kwargs["EMOJI_TYPE"]
        except KeyError:
            emoji_type = None
        
        if emoji_type is not None:
            display_string.append(emoji_type)

        for arg in args:
            display_string.append(arg)
        
        return ' '.join(display_string)  if len(display_string) > 0 else None

    def build_notification(self, display_string=None):
        """
        Returns a serialised json string of a notification
        """
        if display_string is None or len(display_string) < 1:
            raise Exception("display string is required")

        payload = {
            'model': 'notification',
            'userId': self.user.id,
            'display_string': display_string,
            'created_at': int(time.time())
        }
        return json.dumps(payload)
        