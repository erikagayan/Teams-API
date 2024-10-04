from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from teams.models import Team
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TeamViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.moderator_user = User.objects.create_user(
            username="moderator",
            email="moderator@example.com",
            password="modpass",
            is_moderator=True,
            is_staff=True,
        )
        self.manager_user = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="managerpass",
            is_manager=True,
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass"
        )

        self.team = Team.objects.create(name="Team Alpha")

        self.admin_token = self.get_token(self.admin_user)
        self.moderator_token = self.get_token(self.moderator_user)
        self.manager_token = self.get_token(self.manager_user)
        self.user_token = self.get_token(self.regular_user)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_teams_unauthenticated(self):
        url = reverse("team-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team_admin(self):
        url = reverse("team-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_token)
        data = {"name": "Team Beta"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_create_team_regular_user(self):
        url = reverse("team-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        data = {"name": "Team Gamma"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_team_moderator(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.moderator_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_team_manager(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.manager_token)
        data = {"name": "Team Delta"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Team Delta")

    def test_delete_team_regular_user(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.user_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.count(), 1)
