from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*_778f-!zni=w(*-m_2=+q-q020y=^#pyqnq!uuy3ci)7(ysr^'

DEBUG = True

ALLOWED_HOSTS = []

# --- Application definition ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'users',
    'advertisements',
    'tickets',
    'comments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- REST Framework Configuration ---

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# --- Swagger UI Configuration ---

SPECTACULAR_SETTINGS = {
    'TITLE': 'Request Management System API',
    'DESCRIPTION': 'API for managing advertisements and contractor applications',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SECURITY': [{'TokenAuth': []}],
    'APPEND_COMPONENTS': {
        "securitySchemes": {
            "TokenAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Format: Token <your_token_key>"
            }
        }
    },
}

# --- Authentication Backends ---

AUTHENTICATION_BACKENDS = [
    'users.backends.MultiFieldModelBackend',
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_USER_MODEL = "users.User"

# --- Core Settings ---

ROOT_URLCONF = 'RequestManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RequestManagementSystem.wsgi.application'

# --- Database ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Password Validation ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files ---

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'