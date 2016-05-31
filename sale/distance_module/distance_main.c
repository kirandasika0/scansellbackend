#include <Python.h>
#include <math.h>

//Prototypes
// double haversine_km(double lat1, double long1, double lat2, double long2);
// double haversine_mi(double lat1, double long1, double lat2, double long2);

#include "headers.h"

static PyObject* distance_km(PyObject* self, PyObject* args)
{
	double uLatitude, uLongitude;
	double sLatitude, sLongitude;
	double distance;

	if (!PyArg_ParseTuple(args, "dddd", &uLatitude, &uLongitude, &sLatitude, &sLongitude))
	{
		return NULL;
	}
	
	//calling the haversine function
	distance = haversine_km(uLatitude, uLongitude, sLatitude, sLongitude);

	return Py_BuildValue("f", distance);
}

static PyObject* distance_mi(PyObject* self, PyObject* args)
{
	double uLatitude, uLongitude;
	double sLatitude, sLongitude;

	double distance;

	if (!PyArg_ParseTuple(args, "dddd", &uLatitude, &uLongitude, &sLatitude, &sLongitude))
	{
		return NULL;
	}

	distance = haversine_mi(uLatitude, uLongitude, sLatitude, sLongitude);

	return Py_BuildValue("f", distance);
}


static PyMethodDef DistanceMethods[] = {
	{"distance_km", distance_km, METH_VARARGS, "gives distance in km"},
	{"distance_mi", distance_mi, METH_VARARGS, "gives distance in miles"},
	{NULL,NULL,0,NULL}
};

PyMODINIT_FUNC

initdistance_module(void)
{
	(void) Py_InitModule("distance_module", DistanceMethods);
}