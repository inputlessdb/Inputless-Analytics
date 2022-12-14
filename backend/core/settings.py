"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
import dj_database_url
from decouple import config
from unipath import Path
from django.conf import settings
from django.conf.urls.static import static
from base64 import b64decode
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')


ALLOWED_HOSTS = ['*']
MIDDLEWARE = [

    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django_limits.middleware.LimitExceededMiddleware',
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
    'defender.middleware.FailedLoginMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

MODEL_LIMIT_CLASS = 'core.limiter.UserLimiter'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

TEMPLATE_DIR = os.path.join(BASE_DIR, "core/templates")  # ROOT dir for templates
#https://stackoverflow.com/questions/51890820/io-bytesio-object-has-no-attribute-name-for-small-size-file
FILE_UPLOAD_HANDLERS= ["django.core.files.uploadhandler.TemporaryFileUploadHandler"] #

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'  # new for channels


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        'OPTIONS' : {
            'options': '-c search_path=standard,public',
            'sslmode': 'require',
            },
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),

    }
}
####################################################################################
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

HAS_MULTI_TYPE_TENANTS = True
MULTI_TYPE_DATABASE_FIELD = 'type'  # or whatever the name you call the database field

TENANT_TYPES = {
    "public": {  # this is the name of the public schema from get_public_schema_name
        "APPS": [
            'django_tenants',
            'jazzmin',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # shared apps here
            'otp_yubikey',
            'django_otp',
            'django_otp.plugins.otp_static',
            'django_otp.plugins.otp_totp',
            'two_factor',
            'djstripe',
            'customers',
            'honeypot',
            'registration',
            'user_visit',
            'defender',
            'home_public',
            'accounts',
            'ratelimit',
            'chat',
            'channels',  # new

        ],
        "URLCONF": "core.public_urls", # url for the public type here
    },
    "demo": {
        "APPS": [

            'jazzmin',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.messages',
            # type1 apps here
             #your tenant-specific apps
            'crispy_forms',
            'crispy_bootstrap5',
            'bootstrap5', 
            'otp_yubikey',
            'django_otp',
            'django_otp.plugins.otp_static',
            'django_otp.plugins.otp_totp',
            'two_factor',
            'celery',
            'celery_progress',
            'tenant_schemas_celery',
            'app',
            'honeypot',
            'upload',
            'search',
            'user_visit',
            'defender',
            'haystack',
            'djstripe',
            'django_limits',
            'ticket',
            'sendmail',
            'accounts',
            'ratelimit',
            'dashboard',
            'chat',
            'channels',  # new

        ],
        "URLCONF": "core.urls",
    },

    "professional": {
        "APPS": [
            'jazzmin',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.messages',
            # type2 apps here
             #your tenant-specific apps
            'crispy_forms',
            'crispy_bootstrap5',
            'bootstrap5', 
            'otp_yubikey',
            'django_otp',
            'django_otp.plugins.otp_static',
            'django_otp.plugins.otp_totp',
            'two_factor',
            'celery',
            'celery_progress',
            'tenant_schemas_celery',
            'app',
            'honeypot',
            'upload',
            'search',
            'user_visit',
            'defender',
            'haystack',
            'djstripe',
            'django_limits',
            'ticket',
            'payments',
            'sendmail',
            'accounts',
            'ratelimit',
            'dashboard',
            'chat',
            'channels',  # new

        ],
        "URLCONF": "core.urls",
    }
}

INSTALLED_APPS = []
for schema in TENANT_TYPES:
    INSTALLED_APPS += [app for app in TENANT_TYPES[schema]["APPS"] if app not in INSTALLED_APPS]

TENANT_MODEL = "customers.Client" #app.Model

TENANT_DOMAIN_MODEL = "customers.Domain"  #app.Model
SITE_ID = 1
#TENANT_COLOR_ADMIN_APPS = True

DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"
MULTITENANT_RELATIVE_MEDIA_ROOT = ""  # (default: create sub-directory for each tenant)

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
PUBLIC_SCHEMA_URLCONF = 'core.public_urls'
ROOT_URLCONF = ''
#######################################################################################################

HONEYPOT_FIELD_NAME = "jhv*&JHG-8)/kj"
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'), # /app/core/whoosh_index
    },
}
# Add this item, when the database changes, the index will be automatically updated, which is very convenient
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

######################################################################################################

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
###################################################################################################
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        'KEY_FUNCTION': 'django_tenants.cache.make_key',
        'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key',
    }
}

#########################################################################################

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}



##################################################################################################
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'it'
LANGUAGES = [
    ('en','English'),
    ('it', 'Italian')
]

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core/static'),
)

#############################################################

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#############################################################
#spacy model folder
import spacy
MODEL_PATH = os.path.join(BASE_DIR,'model/dd2')
MODEL = spacy.load(MODEL_PATH)
#############################################################
# CELERY STUFF

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_CREATE_MISSING_QUEUES = True

#############################################################
# USER LOGIN
LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py and home_public - namespace are equals -
SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
DISABLE_USERNAME = False
ENABLE_USER_ACTIVATION = True
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = False

###########################################################
# EMAIL BACKEND

#EMAIL_BACKEND = 'django_ses.SESBackend'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp/emails')

###########################################################

#DJSTRIPE API
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY")
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

##########################################################
# RATELIMIT

RATELIMIT_ENABLE=True
RATELIMIT_USE_CACHE=True

###########################################################
import logging.config
from django.utils.log import DEFAULT_LOGGING
# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },

    'handlers': {
        #emits log to the console and file
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'file']
        }
    }
})

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Inputless Myotis Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Inputless Myotis",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Myotis",

    # Logo to use for your site, must be present in static files, used for brand on top left
    #"site_logo": "/img/logo.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome Inputless Analytics Myotis",

    # Copyright on the footer
    "copyright": "Giovanni Errico - Leonardo Trisolini",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://inputless-analytics.com", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        #{"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://inputless-analytics.com", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    #"hide_apps": [''],

    # Hide these models when generating side menu (e.g auth.user)
    #"hide_models": [''],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    #"order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    #"custom_links": {
    #    "books": [{
    #        "name": "Make Messages", 
    #        "url": "make_messages", 
    #        "icon": "fas fa-comments",
    #        "permissions": ["books.view_book"]
    #    }]
    #},

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "single",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}
