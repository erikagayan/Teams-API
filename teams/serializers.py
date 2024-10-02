from rest_framework import serializers
from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members"]
