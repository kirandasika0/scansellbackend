class Location():
    # class contructer
    def __init__(self, latitudeIn, longitudeIn, timestampIn):
        self.latitude = latitudeIn
        self.longitude = longitudeIn
        self.timestamp = timestampIn
        
    def __str__(self):
        return 'Lat:{} Long:{}'.format(self.latitude,self.longitude)