#include <math.h>
#define d2r (M_PI / 180.0)


double haversine_km(double lat1, double long1, double lat2, double long2)
{
    
    double dLat = (lat1 - lat2) * d2r;
    double dLong = (long1 - long2) * d2r;
    
    double a = pow(sin(dLat / 2.0), 2) + cos(lat2 * d2r) * cos(lat1 * d2r) * pow(sin(dLong / 2.0), 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    double d = 6367 * c;
    
    return d;
}

// int main(int argc, char* argv)
// {
// 	double l1 = 17.4509799;
// 	double lg1 = 78.3659762;
// 	double l2 = 17.4898062;
// 	double lg2 = 78.412814;

// 	double answer = haversine_km(l1, lg1, l2, lg2);

// 	printf("%f", answer);

// 	return 0;
// }