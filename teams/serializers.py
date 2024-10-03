from rest_framework import serializers
from teams.models import Team
from users.models import User


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )
    members_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "members", "members_info"]

    def get_members_info(self, obj):
        return [user.username for user in obj.members.all()]
