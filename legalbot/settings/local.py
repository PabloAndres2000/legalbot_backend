from .base import *

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": 5432,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "admin_interface/public/media/")
MEDIA_URL = "/media/"
ALLOWED_HOSTS = ["*"]

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
