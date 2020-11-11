import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Used for cryptographic signing
SECRET_KEY = '^oqhma2=ovj!a(uuhzw+%g95(l!^9_f)#-vjo6b9o)jw$nc*^9'

# Provides debug information if set to true
DEBUG = True

# Can currently run on any host
ALLOWED_HOSTS = ["*"]

# Apps being used in my project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "account",
    "team",
    "tournament",
]

# Middleware being used in my project
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Where the request URL path is initially compared
ROOT_URLCONF = 'mysite.urls'

# Where templates are stored and how they are processed
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

# The database used
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Argon2 is used to hash my passwords
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    ]

# Language debug information is given in
LANGUAGE_CODE = 'en-us'

# Time zone used in creation of records
TIME_ZONE = 'UTC'

# Required for django
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Where my static files are stored (e.g. css, js)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/static/',
]

# Custom backend for authentication
AUTHENTICATION_BACKENDS = ['account.models.MyBackend']

# The model used for users
AUTH_USER_MODEL = "account.User"
