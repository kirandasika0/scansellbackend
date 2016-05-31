#ifndef HEADERS_H
#define HEADERS_H

double haversine_km(double lat1, double long1, double lat2, double long2);
double haversine_mi(double lat1, double long1, double lat2, double long2);

//GPS coordinate struct

typedef struct gpscoordinate {
	double latitude;
	double longitude;
} GPSCoordinate;

#endif