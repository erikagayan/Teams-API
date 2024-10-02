from rest_framework import serializers
from teams.models import Team
from users.serializers import UsernameSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = UsernameSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members"]
