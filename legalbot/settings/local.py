from .base import *

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "legalbot_postgres",
        "PORT": 5432,
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "admin_interface/public/media/")
MEDIA_URL = "/media/"
ALLOWED_HOSTS = ["*"]

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
