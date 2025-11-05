from pathlib import Path

# ------------------------------
# Базовые настройки проекта
# ------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!gxr042kgollb#4zgd!eru&!9#%-h*i3ppvg-*l*@*57uz6fj3'
DEBUG = True
ALLOWED_HOSTS = []
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------
# Установленные приложения
# ------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # <- твое приложение обязательно здесь
]

# ------------------------------
# Мидлвары
# ------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------
# URL конфигурация
# ------------------------------

ROOT_URLCONF = 'myblog.urls'

# ------------------------------
# Настройки шаблонов
# ------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # можно добавить глобальную папку templates, если нужно
        'APP_DIRS': True,  # <- обязательно True для поиска шаблонов внутри apps
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

WSGI_APPLICATION = 'myblog.wsgi.application'

# ------------------------------
# База данных (SQLite по умолчанию)
# ------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------
# Валидация паролей
# ------------------------------

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

# ------------------------------
# Локализация и часовой пояс
# ------------------------------

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------
# Статические файлы
# ------------------------------

STATIC_URL = 'static/'
# Если нужно, можно добавить:
# STATICFILES_DIRS = [BASE_DIR / "static"]

# ------------------------------
# Медиа файлы (картинки, загруженные пользователем)
# ------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------
# ID полей по умолчанию
# ------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ------------------------------
# Переадресация после входа и выхода
# ------------------------------

LOGIN_REDIRECT_URL = '/'  # после успешного входа — на главную
LOGOUT_REDIRECT_URL = '/'  # после выхода — тоже на главную

