from rest_framework import mixins, viewsets, permissions
from teams.models import Team
from teams.serializers import TeamSerializer
from teams.permissions import IsAdminModeratorManager
from rest_framework_simplejwt.authentication import JWTAuthentication


class TeamViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminModeratorManager]
        return [permission() for permission in permission_classes]
