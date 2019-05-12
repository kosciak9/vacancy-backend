import pytest
from mixer.backend.django import mixer

from vacancy.users.models import Availability, Position, Team, User

pytestmark = pytest.mark.django_db


class TestPositon:
    def test_model(self):
        obj = mixer.blend(Position, team=None)
        assert obj.pk == 1, "Should create a Position instance"

    def test_str(self):
        obj = mixer.blend(Position, name="Forward", team=None)
        assert str(obj) == "Forward", "Should return proper Position name"


class TestUser:
    def test_model(self):
        obj = mixer.blend(User, team=None, position=None)
        assert obj.pk, "Should create a User instance"
        obj.save()
        assert obj.auth_token, "Should create Token on save"

    def test_str(self):
        obj = mixer.blend(User, team=None, position=None, username="test_user")
        assert str(obj) == "test_user", "Should return proper username"


class TestTeam:
    def test_model(self):
        user = mixer.blend(User, position=None, team=None)
        obj = mixer.blend(Team, captain=user)
        assert obj.pk == 1, "Should create Team instance"

    def test_str(self):
        user = mixer.blend(User, position=None, team=None)
        obj = mixer.blend(Team, name="Test Team", captain=user)
        assert str(obj) == "Test Team", "Should return proper Team name"


class TestAvailability:
    def test_model(self):
        player = mixer.blend(User, position=None, team=None)
        obj = mixer.blend(Availability, player=player)
        assert obj.pk == 1, "Should create Availability instance"

    def test_str(self):
        player = mixer.blend(User, username="test_user", team=None, position=None)
        obj = mixer.blend(
            Availability, player=player, date="2019-01-01", time="08:30", available=True
        )
        assert str(obj) == "test_user is on 2019-01-01 08:30:00"
        obj = mixer.blend(
            Availability,
            player=player,
            date="2019-01-01",
            time="08:30",
            available=False,
        )
        assert str(obj) == "test_user isn't on 2019-01-01 08:30:00"

    def test_save(self):
        player = mixer.blend(User, position=None, username="test_user", team=None)
        obj = mixer.blend(
            Availability, player=player, date="2019-01-01", time="08:30", available=True
        )
        assert obj.pk == 1
        obj.save()
        obj_new = mixer.blend(
            Availability,
            player=player,
            date="2019-01-01",
            time="08:30",
            available=False,
        )
        assert obj_new.pk == obj.pk
