from distutils.core import Extension, setup

distance_module = Extension('distance_module', sources=['distance_main.c', 'haversine_km.c', 'haversine_mi.c'])

setup(
	name='distance_module',
	version='1.0',
	ext_modules=[distance_module]
)