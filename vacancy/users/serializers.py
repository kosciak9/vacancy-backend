from rest_framework import serializers
from vacancy.users.models import Availability, Position, Team, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "kit_number",
            "position",
            "team",
            "locale",
        )
        read_only_fields = ("auth_token",)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ("pk", "name")


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "pk",
            "name",
            "captain",
            "interval",
            "start_hour",
            "hour_count",
            "days_ahead",
            "priority_days_ahead",
            "priority_fill_date",
            "fill_date",
        )


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ("id", "date", "time", "available", "player")

    def create(self, validated_data):
        answer, created = Availability.objects.get_or_create(
            date=validated_data.get("date", None),
            time=validated_data.get("time", None),
            player=validated_data.get("player", None),
        )

        answer.available = validated_data.get("available", False)
        answer.save()
        print(answer, created)

        return answer
