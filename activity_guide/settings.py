import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

print(f'DEBUG: {os.getenv("DJANGO_DEBUG")}')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG') == 'True'
print(os.getenv('AWS_STORAGE_BUCKET_NAME'))
print("IS_DEBUG:", os.getenv('DJANGO_DEBUG'))

IS_READY = os.getenv('IS_READY') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'activity-guide.fly.dev',
    'activityguide.ca',
    'www.activityguide.ca',
]

CSRF_TRUSTED_ORIGINS = [
    'https://activity-guide.fly.dev',
    'https://activityguide.ca',
    'https://wwww.activityguide.ca',
    'https://cke4.ckeditor.com',
]


# Application definition

INSTALLED_APPS = [
    'layout.apps.LayoutConfig',
    'users.apps.UsersConfig',
    'categories.apps.CategoriesConfig',
    'providers.apps.ProvidersConfig',
    'activities.apps.ActivitiesConfig',
    'members.apps.MembersConfig',
    'ads',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_htmx',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'phonenumber_field',
    'ckeditor',
    'ckeditor_uploader',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'layout.middleware.HTMXMiddleware',
    'layout.middleware.IsReadyMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'activity_guide.urls'

default_loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

cached_loaders = [('django.template.loaders.cached.Loader', default_loaders)]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'layout' / 'templates' / 'layout'],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': default_loaders if DEBUG else cached_loaders,
            'builtins': [
                'layout.templatetags.dict_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'activity_guide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=False
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTH_PROFILE_MODULE = 'users.UserProfile'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

CKEDITOR_UPLOAD_PATH = "uploads/"

print('DEBUG:', DEBUG)
if DEBUG:
    ...
else:
    STATIC_URL = f'https://{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

DEFAULT_FROM_EMAIL = os.getenv('CONTACT_FROM_EMAIL')
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME')

AWS_SES_REGION_ENDPOINT = os.getenv('AWS_SES_REGION_ENDPOINT')

CONTACT_ENABLED = os.getenv('CONTACT_ENABLED') == 'True'

LOGIN_URL = '/users/login'
LOGIN_REDIRECT_URL = '/members/dashboard'

PAGE_SIZE = 10

MAX_ADS_PER_SECTION = 4

MAX_ITEMS_IN_HOMEPAGE_CAROUSEL = int(os.getenv('MAX_ITEMS_IN_HOMEPAGE_CAROUSEL'))
