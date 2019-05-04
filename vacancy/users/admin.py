from django.contrib import admin

from .models import User, Team, Position

admin.site.register(Position)
admin.site.register(Team)
admin.site.register(User)
