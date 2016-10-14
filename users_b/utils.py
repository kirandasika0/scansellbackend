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
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude
    try:
        response = json.loads(requests.get(url).content)
    except:
        return_response = "nil"
    #getting the info that we need.
    for obj in response["results"][0]["address_components"]:
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
            
    return ''.join(locale).upper()
    
def password_generator(password):
    s = Signer()
    hashPassword = s.sign(password)
    hashPassword = hashPassword.split(':')
    return hashPassword[1]