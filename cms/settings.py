import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-l+h5q-)9z0-gsak2r@@er_3ck3-=v8+-j@wtuu$(91&g*t-02b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "login",
    "administracion",
    "roles",
    "publicaciones",
    "canvan",
    "PIL",
    "tinymce",    
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

ROOT_URLCONF = "cms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = "cms.wsgi.application"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'  # o el código de idioma adecuado para tu aplicación

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'login.Usuario'
LOGIN_URL = 'login:inicio_sesion'  # Configura la URL de inicio de sesión
LOGIN_REDIRECT_URL = 'login:perfil'  # Configura la URL de redirección después del inicio de sesión

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "es_ES",
    "content_css": [
        "https://fonts.googleapis.com/css?family=Proxima+Nova:400,400i,700,700i,900,900i&display=swap",
        "https://fonts.googleapis.com/css?family=Helvetica&display=swap",
        "https://fonts.googleapis.com/css?family=Georgia&display=swap",
        "https://fonts.googleapis.com/css?family=Cambria&display=swap",
        "https://fonts.googleapis.com/css?family=Charter&display=swap",
        "https://fonts.googleapis.com/css?family=Marath+Sans&display=swap",
        "https://fonts.googleapis.com/css2?family=Notable&display=swap",  # Agrega el enlace de la fuente Noe aquí
        "https://fonts.googleapis.com/css?family=Fell+Types&display=swap",  # Agrega el enlace de la fuente Fell aquí
        "https://fonts.googleapis.com/css?family=Sohne&display=swap",  # Agrega el enlace de la fuente Sohne aquí
        "https://fonts.googleapis.com/css?family=Kievit&display=swap",  # Agrega el enlace de la fuente Kievit aquí
        "https://fonts.googleapis.com/css2?family=Fuggles&display=swap",
        "https://fonts.googleapis.com/css2?family=Elsie:wght@400;900&family=Fuggles&display=swap",
        "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600;1,700;1,800;1,900&display=swap",
        "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap",
        "https://fonts.googleapis.com/css2?family=Ibarra+Real+Nova&display=swap",
    ],

    "font_formats": (
    "Proxima Nova=proxima_nova;"
    "Helvetica=Helvetica;"
    "Georgia=Georgia;"
    "Cambria=Cambria;"
    "Charter=Charter;"
    "Notable=Notable;"
    "Marath Sans=Marath Sans;"
    "Fuggles=Fuggles;"
    "Elsie=Elsie;"
    "Playfair Display=Playfair Display;"
    "Lora=Lora;"
    "Ibarra Real Nova=Ibarra Real Nova;"
    ),

}
TINYMCE_SPELLCHECKER = True

ALLOWED_HOSTS = ["localhost","127.0.0.1"] # Solo para desarrollo, cambia a tus necesidades de producción

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cms_bd',  # Nombre de la base de datos PostgreSQL
        'USER': 'postgres',  # Usuario PostgreSQL
        'PASSWORD': '12345',  # Contraseña PostgreSQL
        'HOST': 'db',  # Nombre del servicio de la base de datos en Docker Compose
        'PORT': '5432',  # Puerto por defecto de PostgreSQL
    }
}

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080","http://localhost:8000","http://localhost:80",
"http://127.0.0.1:80","http://127.0.0.1:8080","http://127.0.0.1:8000"]
