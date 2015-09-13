import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '$=x_)b##pba18^i(5=wtsw@^$plpg23pwaf@8_c!s!5b9ndhxr'
DEBUG = os.environ.get('DEBUG', '') != '' or os.uname().sysname == 'Darwin'
ALLOWED_HOSTS = ['localhost', 'losers.temp.io']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'losers',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'losers.urls'
WSGI_APPLICATION = 'losers.wsgi.application'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'losers.db'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'losers',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Sets the "error" message tag to class "danger", for Bootstrap.
MESSAGE_TAGS = {
    40: 'danger',
}

# Email

DEFAULT_FROM_EMAIL = 'noreply@losers.temp.io'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pipeline

PIPELINE_CSS = {
    'losers': {
        'source_filenames': (
            'css/losers.css',
        ),
        'output_filename': 'losers.css',
    },
}

PIPELINE_JS = {
    'losers': {
        'source_filenames': (
        ),
        'output_filename': 'losers.js',
    },
}
