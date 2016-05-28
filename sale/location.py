class Location():
    # class contructer
    def __init__(self, latitudeIn, longitudeIn, timestampIn):
        self.latitude = latitudeIn
        self.longitude = longitudeIn
        self.timestamp = timestampIn
        
    def getLatitude(self):
        return self.latitude
        
    def getLongitude(self):
        return self.longitude
        
    def getTimestamp(self):
        return self.timestamp
        
    def setLatitude(self, latitudeIn):
        self.latitude = latitudeIn
        
    def setLongitude(self, longitudeIn):
        self.longitudeIn = longitudeIn
        
    def setTimestamp(self, timestampIn):
        self.timestamp = timestampIn
        
    def __str__(self):
        return 'Lat:{} Long:{}'.format(self.latitude,self.longitude)