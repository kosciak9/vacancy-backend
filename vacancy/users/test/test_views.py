import pytest
from vacancy.users.models import User, Team, Position, Availability
from rest_framework.test import APITestCase
from rest_framework import status

from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestPermissions(APITestCase):
    def setUp(self):
        """
        we setup environement with:
        group A (standard): team, user, position and availability
        group B (other): team, user, position and availability
        group A captain (user) shouldn't be allowed to see objects from group B
        """

        # group A
        self.standard_user = User.objects.create_user(
            "standard_user", "jan@kowalski.com", "hunter2"
        )
        self.standard_team = mixer.blend(Team, captain=self.standard_user)
        self.standard_team.save()
        self.standard_user.team = self.standard_team
        self.standard_user.save()
        self.standard_position = mixer.blend(Position, team=self.standard_team)
        self.standard_position.save()
        self.standard_availability = mixer.blend(
            Availability, player=self.standard_user
        )
        self.standard_availability.save()

        # group B
        self.other_user = User.objects.create_user(
            "other_user", "jan@kowalski.com", "hunter2"
        )
        self.other_team = mixer.blend(Team, captain=self.other_user)
        self.other_team.save()
        self.other_user.team = self.other_team
        self.other_user.save()
        self.other_position = mixer.blend(Position, team=self.other_team)
        self.other_position.save()
        self.other_availability = mixer.blend(Availability, player=self.other_user)
        self.other_availability.save()
        self.client.login(username="standard_user", password="hunter2")

    def test_get_team(self):
        response = self.client.get(f"/v1/teams/{self.standard_team.id}/")
        assert str(self.standard_team.id) in response.content.decode()
        response = self.client.get(f"/v1/teams/{self.other_team.id}/")
        assert str(self.other_team.id) not in response.content.decode()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user(self):
        response = self.client.get(f"/v1/users/{self.standard_user.id}/")
        assert str(self.standard_user.id) in response.content.decode()
        response = self.client.get(f"/v1/users/{self.other_user.id}/")
        assert str(self.other_user.id) not in response.content.decode()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_availability(self):
        response = self.client.get(f"/v1/availability/{self.standard_availability.id}/")
        assert str(self.standard_availability.id) in response.content.decode()
        response = self.client.get(f"/v1/availability/{self.other_availability.id}/")
        assert str(self.other_availability.id) not in response.content.decode()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_team(self):
        response = self.client.post(
            f"/v1/teams/", {"name": "Test Team", "captain": self.standard_user.id}
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_user(self):
        response = self.client.post(f"/v1/users/", {"username": "test_user"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_availability(self):
        response = self.client.post(
            f"/v1/availability/",
            {
                "available": True,
                "player": self.standard_user.id,
                "date": "2019-01-01",
                "time": "08:30:00",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_patch_team(self):
        response = self.client.patch(
            f"/v1/teams/{self.standard_team.id}/", {"name": "Standard Team"}
        )
        assert response.status_code == status.HTTP_200_OK
        response = self.client.patch(
            f"/v1/teams/{self.other_team.id}/", {"name": "Standard Team"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_user(self):
        response = self.client.patch(
            f"/v1/users/{self.standard_user.id}/", {"username": "test_user"}
        )
        assert response.status_code == status.HTTP_200_OK
        response = self.client.patch(
            f"/v1/users/{self.other_user.id}/", {"username": "test_user"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_availability(self):
        response = self.client.patch(
            f"/v1/availability/{self.standard_availability.id}/", {"available": False}
        )
        assert response.status_code == status.HTTP_200_OK
        response = self.client.patch(
            f"/v1/availability/{self.other_availability.id}/", {"available": False}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
