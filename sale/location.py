class Location():
    # class contructer
    def __init__(self, latitudeIn, longitudeIn, timestampIn=None):
        self.latitude = float(latitudeIn)
        self.longitude = float(longitudeIn)
        self.timestamp = timestampIn
        
    def __str__(self):
        return 'Lat:{} Long:{}'.format(self.latitude,self.longitude)