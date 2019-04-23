from datetime import date, timedelta, time, datetime 

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from xintai.users.models import Availability, Position, Team, User
from xintai.users.permissions import OwnTeamOrPermissionDenied
from xintai.users.serializers import (AvailabilitySerializer,
                                      PositionSerializer, TeamSerializer,
                                      UserSerializer)


class AvailabilityViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user availablity
    """
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('date', 'time', 'player', )


@api_view(['GET'])
def per_user_priority_availability(request):
    player = request.user
    start_hour = player.team.start_hour
    interval = player.team.interval  # shadow this later
    interval = timedelta(hours=interval.hour, minutes=interval.minute)
    hour_count = player.team.hour_count
    days_ahead = player.team.priority_days_ahead
    iteration_date = date.today()
    priority_availability = []
    for _i in range(days_ahead):
        day = { 'date': iteration_date.isoformat(), 'availability': [] }
        iteration_time = time(hour=start_hour.hour, minute=start_hour.minute)
        for _j in range(hour_count):
            try:
                availability = Availability.objects.get(
                    date=iteration_date, time=iteration_time, player=player
                )
            except Availability.DoesNotExist:
                availability = Availability(
                    date=iteration_date, time=iteration_time, player=player
                )
                availability.save()
            day['availability'].append(
                AvailabilitySerializer(availability).data
            )
            iteration_time = (datetime.combine(
                date.today(), iteration_time) + interval).time()
            # iteration_time = iteration_time + interval
        priority_availability.append(day)
        iteration_date = iteration_date + timedelta(days=1)
    return Response(priority_availability)


class TeamViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', )


class PositionViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives positions
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', )


class UserViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, OwnTeamOrPermissionDenied,)
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('username', )
