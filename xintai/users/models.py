import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

from rest_framework.authtoken.models import Token


class Position(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AdditionalPerk(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    captain = models.ForeignKey(related_name='Captain',
                                to='User',
                                on_delete=models.CASCADE)
    interval = models.TimeField(default='1:30')
    start_hour = models.TimeField(default='8:30')
    hour_count = models.IntegerField(default=10)
    days_ahead = models.IntegerField(default=28)
    priority_days_ahead = models.IntegerField(default=7)

    def priority_fill_date(self):
        current_day = datetime.now().replace(hour=0, minute=0, second=0,
                                             microsecond=0)
        current_weekday = current_day.isocalendar()[2] - 1  # start on Monday
        delta = timedelta(days=current_weekday)
        current_day = current_day - delta
        delta = timedelta(days=self.priority_days_ahead)
        current_day = current_day + delta
        return current_day

    def fill_date(self):
        current_day = datetime.now().replace(hour=0, minute=0, second=0,
                                             microsecond=0)
        current_weekday = current_day.isocalendar()[2] - 1  # start on Monday
        delta = timedelta(days=current_weekday)
        current_day = current_day - delta
        delta = timedelta(days=self.days_ahead)
        current_day = current_day + delta
        return current_day

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    position = models.ForeignKey(Position, null=True, on_delete=models.CASCADE)
    kit_number = models.IntegerField(default=99)
    team_admin = models.BooleanField(default=False)

    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    additional_perks = models.ManyToManyField(AdditionalPerk, blank=True)
    locale = models.CharField(max_length=2, choices=(
        ('en', 'English'),
        ('pl', 'Polski'),
    ), default='pl')

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Availability(models.Model):
    date = models.DateField()
    time = models.TimeField()
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        sep = ' isn\'t on '
        if self.available:
            sep = ' is on '
        return (str(self.player) + sep + str(self.date) + ' ' + str(self.time))

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                combination = Availability.objects.get(
                    date=self.date,
                    time=self.time,
                    player=self.player
                )
                self.pk = combination.pk
            except Availability.DoesNotExist:
                pass
        super(Availability, self).save(*args, **kwargs)
