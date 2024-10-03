from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from teams.models import Team
from teams.permissions import is_admin_moderator_manager

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), required=False, allow_null=True
    )
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "team",
            "team_name",
            "is_moderator",
            "is_manager",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_moderator": {"required": False},
            "is_manager": {"required": False},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        # Check if the current user is an administrator, moderator or manager
        if not is_admin_moderator_manager(user):
            # Normal users cannot set these flags
            if "is_moderator" in attrs or "is_manager" in attrs:
                raise serializers.ValidationError(
                    "You do not have permission to set moderator or manager status."
                )
        return attrs

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def create(self, validated_data):
        team = validated_data.pop("team", None)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_moderator=validated_data.get("is_moderator", False),
            is_manager=validated_data.get("is_manager", False),
        )
        if team:
            user.team = team
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        team = validated_data.pop("team", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        if team is not None:
            instance.team = team

        try:
            instance.save()
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

        return instance


class UsernameSerializer(serializers.ModelSerializer):
    """Return users username"""

    class Meta:
        model = User
        fields = ["username"]
