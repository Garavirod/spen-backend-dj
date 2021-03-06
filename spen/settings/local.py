from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

""" Rutas estáticas """
STATIC_URL = '/static/'
""" Archivos estáticos """
STATIC_FILES_DIRS = [BASE_DIR.child('static')]
""" Archivos mnultimedia """
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')