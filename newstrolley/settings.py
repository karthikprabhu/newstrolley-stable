import localsettings

DEBUG = localsettings.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Karthik Prabhu', 'k.karthik.prabhu@gmail.com'),
    ('Divyansh Prakash', 'divyansh.prakash@yahoo.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + localsettings.DB_ENGINE, # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': localsettings.DB_NAME,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': localsettings.DB_USER,
        'PASSWORD': localsettings.DB_PASSWORD,
        'HOST': localsettings.DB_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = localsettings.ALLOWED_HOSTS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = localsettings.PROJECT_ROOT_DIR + 'newsreader/static/newsreader/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/static/newsreader/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = localsettings.STATIC_ROOT

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uydp-5u0_2^&4x$@c-oygn+5aw%k6ss0hkd#%g%of8@im+0w7y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'newstrolley.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'newstrolley.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'newsreader',
    'accounts',
    'dajaxice',
    'taggit',
    'tags',
    'feeds',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt' : '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'debug_file': { #For use during debugging. Contains low level information
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'newstrolley.debug.log',
            'formatter': 'verbose',
        },
        'info_file': { #Contains basic information of the operations. This file will be reset every few days
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'newstrolley.info.log',
            'formatter': 'verbose',
        },
        'error_file': { #Only errors and warnings will be logged to this file
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'newstrolley.error.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'dajaxice': {
            'handlers': ['mail_admins', 'debug_file', 'info_file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'newstrolley': {
            'handlers': ['debug_file', 'info_file', 'error_file'],
            'level': 'DEBUG'
        },
        'newsreader': {
            'handlers': ['debug_file', 'info_file', 'error_file'],
            'level': 'DEBUG'
        },
        'feeds': {
            'handlers': ['debug_file', 'info_file', 'error_file'],
            'level': 'DEBUG'
        },
        'accounts': {
            'handlers': ['debug_file', 'info_file', 'error_file'],
            'level': 'DEBUG'
        },
        'tags': {
            'handlers': ['debug_file', 'info_file', 'error_file'],
            'level': 'DEBUG'
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'accounts.NTUser'

CONTENT_TYPES = ['image', 'video']
# 0.5MB - 524288
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "524288"

DAJAXICE_MEDIA_PREFIX = "dajaxice"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': localsettings.PROJECT_ROOT_DIR + 'cache',
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)