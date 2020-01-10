
import os
from os.path import join
from tempfile import gettempdir

DISPLAY_EXCEPTIONS_BASE_TEMPLATE = 'exceptions/base.html'  # optional setting

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'very_secret_key'

DEBUG = False

INSTALLED_APPS = (
	'display_exceptions',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'test_app',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'display_exceptions.DisplayExceptionMiddleware',
)

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
		'NAME': '{0:s}/{1:s}'.format(gettempdir(), 'tmp_display_exceptions_db.sqlite3'),
	}
}

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

ALLOWED_HOSTS = ['*']


