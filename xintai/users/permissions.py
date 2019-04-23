from rest_framework import permissions
from xintai.users.models import Availability, Team, User


class OwnTeamOrPermissionDenied(permissions.BasePermission):
    """
    Object-level permission meant to be used for everything.
    Allows only owner or team admin to modify properties.
    Disallows seeing other teams' availablity or other objects
    if you're not a member.
    """

    def has_object_permission(self, request, view, obj):
        permission = False

        if type(obj) is User:
            permission = request.user == obj

        if type(obj) is Availability:
            permission = request.user == obj.player

        # safe methods are read only
        if request.method in permissions.SAFE_METHODS:
            if type(obj) is User:
                permission = request.user.team == obj.team

            if type(obj) is Availability:
                permission = request.user.team == obj.player.team

            if type(obj) is Team:
                permission = request.user.team == obj

        if request.user.team_admin:
            if type(obj) is User:
                permission = request.user.team == obj.team

            if type(obj) is Availability:
                permission = request.user.team == obj.player.team

            if type(obj) is Team:
                permission = request.user.team == obj

        return permission
