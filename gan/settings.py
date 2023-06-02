import os
from pathlib import Path
from allauth.account import app_settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-fuujk5n=sy!qc)((rf0a&y*d=a4*p@2lgv_ih-42_=-w@+r$y("

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "ganapp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
            str(BASE_DIR / "templates/account"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "gan.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "ganapp/static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "account_login"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# Kimlik doğrulama işlemleri
SITE_ID = 1  # varsayılan site kimliği (genellikle 1'dir)

DEFAULT_FROM_EMAIL = (
    "GANAPP@gmail.com"  # E-postaların gönderileceği varsayılan e-posta adresi
)
ACCOUNT_EMAIL_VERIFICATION = (
    "mandatory"  # Kullanıcının e-posta adresini doğrulama zorunluluğu
)
ACCOUNT_EMAIL_SUBJECT_PREFIX = "GANAPP e-posta doğrulama"  # E-posta konusu için önek
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"  # SMTP e-posta gönderimi için
)
EMAIL_HOST = "smtp.gmail.com"  # SMTP sunucu adresi
EMAIL_PORT = 587  # SMTP sunucu bağlantı noktası
EMAIL_HOST_USER = "sariakce.busra.nur@gmail.com"  # SMTP sunucusu kullanıcı adı
EMAIL_HOST_PASSWORD = "fsjtmadwgqbiixzt"  # SMTP sunucusu parolası
EMAIL_USE_TLS = True  # TLS kullanarak e-posta gönderimi


assert (
    app_settings.AUTHENTICATION_METHOD
    in app_settings.AuthenticationMethod.__dict__.values()
)
assert isinstance(app_settings.EMAIL_REQUIRED, bool)
assert isinstance(app_settings.UNIQUE_EMAIL, bool)
assert (
    app_settings.EMAIL_VERIFICATION
    in app_settings.EmailVerificationMethod.__dict__.values()
)
assert (
    isinstance(app_settings.USER_MODEL_USERNAME_FIELD, str)
    or app_settings.USER_MODEL_USERNAME_FIELD is None
)
assert (
    app_settings.MAX_EMAIL_ADDRESSES is None
    or isinstance(app_settings.MAX_EMAIL_ADDRESSES, int)
    and app_settings.MAX_EMAIL_ADDRESSES > 0
)
