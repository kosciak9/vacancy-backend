import os

from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn",)
