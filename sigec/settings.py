import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# try get custom settings
try:
    with open(os.path.join(BASE_DIR, "sigec", "mysettings.json"), encoding='utf-8') as f:
        USER_SETTINGS = json.load(f)
except:
    USER_SETTINGS = {}

VERSION = "1.9.12"
'''
    VERSION:    1   - SIGEC FUNCTIONS
    RELEASE:    9   - SAAS
    FIX:        12   - OFFER GENERATOR LINK
'''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p3o3or6fsa-%!!go0=iae9=+c&zl3l@9(2p61$&5r*5e7fk&(1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = USER_SETTINGS.get('DEBUG', True)

ALLOWED_HOSTS = USER_SETTINGS.get('ALLOWED_HOSTS', ['*'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Propias
    'apps.data',
    'apps.cotizaciones',
    'apps.reparaciones',
    'apps.saas',

    # ... other apps
    'dynamic_raw_id',
    'crispy_forms',
    
    #'admin_footer',    #django-admin-footer
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sigec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sigec.wsgi.application'

# ADMIN_FOOTER_DATA = {
#   'site_url': 'http://sv-pruebas/sigec',
#   'site_name': 'SIGeC',
#   'period': '{}'.format(datetime.now().year),
#   'version': 'v{} - '.format(VERSION)
# }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#Si se encuentra la config en variables de sistema, se toma dicha configuracion. 
#Caso contrario, se toma la por defecto
DATABASES = USER_SETTINGS.get('DATABASES') or {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = USER_SETTINGS.get('LANGUAGE_CODE', 'es-ar')
TIME_ZONE = USER_SETTINGS.get('TIME_ZONE', 'America/Argentina/Buenos_Aires')

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'statics_pub')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_uploads')

MONEDA_DEFAULT = 'U$D'
FILE_CLIENTES = "{}\\import\\clientes.csv".format(BASE_DIR)
FILE_PRODUCTOS = "{}\\import\\productos.csv".format(BASE_DIR)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


#FOR SAAS OFFERS - porcentual values
FACTOR_TRANSFER_PRICE = 1.51
UE_TO_USD = 1.11
MANTENIMIENTO_ANUAL = 1.18
IMPLEMENTACION = 0.25
COMISION_VENTAS = 0.05

PORCENTAJE_COSTO = 20  #porcentual value

FINANCING = (
    ('36', '36 meses'),
    ('48', '48 meses'),
)
HARDWARE = (
    ('p', 'SPEC'),
    ('t', 'Terceros'),
)

SELLER = (
    ('0', 'End User'),
    ('1', 'Partner'),
    ('2', 'Mayorista'),
)

PRICING_MANAGEMENT = (
    ('vf', 'Valor fijo'),
    ('vm', 'Valor fijo Mensual'),
    ('rp', 'Rangos de precio'),
    ('rm', 'Rangos de precio Mensual'),
    ('pu', 'Variable por cantidad'),
    ('pm', 'Variable por cantidad Mensual'),
)
