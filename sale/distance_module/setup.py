from distutils.core import Extension, setup
from Cython.Distutils import build_ext

distance_module = Extension('distance_module', sources=['../../distance_main.c', 'haversine_km.c', 'haversine_mi.c'])

setup(
	cmdclass={'build_ext': build_ext},
	ext_modules=[distance_module]
)