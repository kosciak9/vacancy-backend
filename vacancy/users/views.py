from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from vacancy.users.models import Availability, Position, Team, User
from vacancy.users.permissions import OwnTeamOrPermissionDenied
from vacancy.users.serializers import (
    AvailabilitySerializer,
    PositionSerializer,
    TeamSerializer,
    UserSerializer,
)


class AvailabilityViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user availablity
    """

    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("date", "time", "player")


class TeamViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives teams
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("name",)


class PositionViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives positions
    """

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user accounts
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("username",)
