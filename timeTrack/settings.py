"""
Django settings for timeTrack project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from multisite import SiteID

SITE_ID = SiteID(default=1)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2*kw+#k1^v#w#_3=ki8=ajow^+8p8t6&xwp-7f$y21%jdo_w$a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.149','127.0.0.1','190.92.148.76','http://sunmantime.com/']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'home.apps.HomeConfig',
    'register.apps.RegisterConfig',
    'django_user_agents',
    'multisite',
    'djangocms_multisite',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:8000',
    }
}

USER_AGENTS_CACHE = 'default'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'multisite.middleware.DynamicSiteMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'djangocms_multisite.middleware.CMSMultiSiteMiddleware',
]

ROOT_URLCONF = 'timeTrack.urls'

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
            'loaders': [
                'multisite.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'timeTrack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
MULTISITE_CMS_URLS={
    'www.example.com': 'tests.test_utils.urls1',
    'www.example2.com': 'tests.test_utils.urls2',
}
MULTISITE_CMS_ALIASES={
    'www.example.com': ('alias1.example.com', 'alias2.example.com',),
    'www.example2.com': ('alias1.example2.com', 'alias2.example2.com',),
}
MULTISITE_CMS_FALLBACK='www.example.com'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

CRISPY_TEMPLATE_PACK="bootstrap4"

LOGIN_REDIRECT_URL="/"
LOGOUT_REDIRECT_URL="/login"
SESSION_EXPIRE_AT_BROWSER_CLOSE= True
SESSION_COOKIE_AGE = 600 # 5 seconds for testing
SESSION_SAVE_EVERY_REQUEST = True

MULTISITE_CMS_URLS={
    'sunmantime.com': 'tests.test_utils.urls1',
}
MULTISITE_CMS_ALIASES={
    'sunmantime.com':  ('alias1.example.com'),
}
MULTISITE_CMS_FALLBACK='www.example.com'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
