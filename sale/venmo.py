import json
from users_b.models import User
from requests import get, post


class VenmoWrapper():
    def __init__(self, userIn, memcacheIn):
        self.user = VenmoUser(userIn)
        self.memcache = memcacheIn

    def isAuthenticated(self):
        """
        This method checks if the user is authenticated with our Venmo app.

        :return: bool
        """
        pass

    def authenticateUser(self):
        """
        This method authenticates a user with the venmo credentials provided.
        Most of the authentication is done in the client side until access
        token is received.

        :return: json
        """
        pass

    def chargeUser(self, otherUser):
        """
        This method charges the user passed in the argument of the method.
        Returns a json string contain some information about the transaction.

        Arguments:
        - otherUser = a users_b.models.User object. A reference to chargable
        user.

        :return: json
        """
        pass



class VenmoUser():
    def __init__(self, userIn=None, accessTokenIn=None):
        self.user = userIn
        self.accessToken = accessTokenIn

    def __str__(self):
        return self.user.username + "-" + self.accessToken

    def serialize(self):
        response = {
            'pk': self.user.pk,
            'user_id': self.user.user_id,
            'access_token': self.accessToken
        }
        return response

    def deserialize(self, dataIn):
        self.user = User.objects.get(pk=dataIn['pk'])
        self.accessToken = dataIn['access_token']
        return True


class VenmoRequest():
    def __init__(self, userIn, chargeIn=0, autoCharge=False):
        self.user = userIn
        self.charge = chargeIn
        self.autoCharge = False

    def __str__(self):
        return self.user + "-" + str(self.charge)

    def serialize(self):
        response = {
            'user': self.user.serialize(),
            'charge': str(self.charge),
            'auto_charge': self.autoCharge
        }
        return response

    def deserialize(self, dataIn):
        self.user = VenmoUser()
        self.user.deserialize(dataIn['user'])
        self.charge = dataIn['charge']
        self.autoCharge = dataIn['auto_charge']
        return True
