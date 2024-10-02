from rest_framework import mixins, viewsets
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
    permission_classes = [IsAdminModeratorManager]
