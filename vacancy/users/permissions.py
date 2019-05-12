from rest_framework import permissions

from vacancy.users.models import Availability, Position, Team, User


class OwnTeamOrPermissionDenied(permissions.BasePermission):
    """
    Object-level permission meant to be used for everything.
    Allows only owner or team admin to modify properties.
    """

    def has_object_permission(self, request, view, obj):
        permission = False

        if (
            request.method in permissions.SAFE_METHODS
        ) or request.user.team.captain == request.user:
            if type(obj) is Availability:
                permission = request.user.team == obj.player.team

            elif type(obj) is User or type(obj) is Position:
                permission = request.user.team == obj.team

            elif type(obj) is Team:
                permission = request.user.team == obj

        return permission
