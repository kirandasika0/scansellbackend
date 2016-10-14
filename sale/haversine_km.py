import math
D2_R = ((math.pi) / 180.0)
def haversine_km(refLocation, saleLocation):
    dLat = (refLocation.latitude - saleLocation.latitude) * D2_R
    dLong = (refLocation.longitude - saleLocation.longitude) *D2_R
    
    a = math.pow(math.sin(dLat / 2.0), 2) + math.cos(saleLocation.latitude * D2_R) * math.cos(refLocation.latitude * D2_R) * math.pow(math.sin(dLong / 2.0), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6367 * c
