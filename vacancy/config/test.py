import os

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Test(Common):
    DEBUG = True
    SECRET_KEY = "DJANGO_TEST_ENVIRONENT"

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS

    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    }

    # Mail
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
