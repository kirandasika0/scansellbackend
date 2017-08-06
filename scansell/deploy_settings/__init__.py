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
