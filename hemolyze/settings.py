from pathlib import Path
from decouple import config
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-b7%fkrf8py&oyr#!zy2#il1&edp&86k0dbcjxe*%nim%98)dcc'
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', "localhost"]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://hemolyze-woad.vercel.app',
]
# Application definition
# 
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'djoser',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'drf_yasg',
    "debug_toolbar",
    'api',
    'user',
    'dashboard',
    'blood_request',
    'django_filters',
]
# 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]
ROOT_URLCONF = 'hemolyze.urls'
BACKEND_URL = config('BACKEND_URL')
FRONTEND_URL = config('FRONTEND_URL')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hemolyze.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DBname'),
        'USER': config('DBuser'),
        'PASSWORD': config('DBpassword'),
        'HOST': config('DBhost'),
        'PORT': config('DBport'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
AUTH_USER_MODEL ='user.CustomUser'

STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# Add JWT settings
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'blood_request.exceptions.custom_exception_handler'
}
SIMPLE_JWT ={
'AUTH_HEADER_TYPES':('JWT',),
"ACCESS_TOKEN_LIFETIME":timedelta(days=2)
}
DJOSER = {
    'EMAIL_FRONTEND_PROTOCOL':config('FRONTEND_PROTOCOL'),
    'EMAIL_FRONTEND_DOMAIN':config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME':'Hemolyze',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {
        'user_create': 'user.serializers.UserCreateSerializer',
        'user': 'user.serializers.UserSerializer',
        'current_user': 'user.serializers.UserSerializer',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST') 
EMAIL_USE_TLS = config('EMAIL_USE_TLS',cast=bool) 
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
