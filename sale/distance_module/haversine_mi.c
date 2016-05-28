#include <math.h>
#define d2r (M_PI / 180.0)

double haversine_mi(double lat1, double long1, double lat2, double long2)
{   
    
    double dLat = (lat1 - lat2) * d2r;
    double dLong = (long1 - long2) * d2r;
    
    double a = pow(sin(dLat / 2.0), 2) + cos(lat2 * d2r) * cos(lat1 * d2r) * pow(sin(dLong / 2.0), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double d = 3956 * c;
    
    return d;

}