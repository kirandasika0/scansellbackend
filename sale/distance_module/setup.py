from distutils.core import Extension, setup
from Cython.Distutils import build_ext

distance_module = Extension('distance_module', sources=['sale/distance_module/distance_main.c', 'sale/distance_module/haversine_km.c', 'sale/distance_module/haversine_mi.c'])

setup(
	name='distance_module',
	version='0.1',
	cmdclass={'build_ext': build_ext},
	ext_modules=[distance_module]
)