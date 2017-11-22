import string
import random
import requests
import json
from django.core.signing import Signer

def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_locale(latitude, longitude):
    locale = []
    #sending request to google to create locale
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(latitude) + "," + str(longitude)
    try:
        response = json.loads(requests.get(url).content)
    except:
        raise ValueError("no data provided from google.")
    #getting the info that we need.
    try:
        goog_response = response["results"][0]["address_components"]
    except IndexError:
        raise ValueError("response could not be serialized")
    
    for obj in goog_response:
        if "route" in obj["types"]:
            locale.append(obj["long_name"])
        if "administrative_area_level_3" in obj["types"]:
            locale.append(obj["long_name"])
        if "locality" in obj["types"]:
            locale.append(obj["long_name"])
        if "administrative_area_level_2" in obj["types"]:
            locale.append(obj["long_name"])
        if "administrative_area_level_1" in obj["types"]:
            locale.append(obj["short_name"])
    return ','.join(locale).upper()

def password_generator(password):
    s = Signer()
    hashPassword = s.sign(password)
    hashPassword = hashPassword.split(':')
    return hashPassword[1]











def sort_usernames(users):
    ''' Sorts all the usernames in ascending order.
    Keyword-args:
    users - a list of all user objects to sort

    return: list (a list containing the sorted usernames)
    '''
    result = []
    if len(users) == 1:
        return users

    mid = len(users) / 2
    y = sort_usernames(users[:mid])
    z = sort_usernames(users[mid:])
    i = 0
    j = 0

    while i < len(y) and j < len(z):
        if y[i].compareTo(z[j]):
            result.append(z[j])
            j += 1
        else:
            result.append(y[i])
            i += 1
    result += y[j:]
    result += z[j:]
    return result


def contains_user(username, users):
    lo = 0
    hi = len(users) - 1

    mid = lo + (hi - lo) / 2
    while (lo <= hi):
        if username < users[mid].username:
            hi = mid - 1
        elif username > users[mid].username:
            lo = mid + 1
        else:
            return True

    return False
