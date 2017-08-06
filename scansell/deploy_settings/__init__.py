"""
All deployment settings
"""
from scansell.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '.herokuapp.com'
]

SECRET_KEY = get_env_variable("SECRET_KEY")
DATABASES["default"] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': get_env_variable("DATABASE_MYSQL_NAME"),
    'USER': get_env_variable("DATABASE_MYSQL_NAME"),
    'PASSWORD': get_env_variable("DATABASE_MYSQL_PASSWORD"),
    'HOST': get_env_variable("DATABASE_MYSQL_HOST")
}
STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
