from django.test import TestCase
from teams.models import Team
from users.models import User
from teams.serializers import TeamSerializer


class TeamSerializerTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )
        self.team = Team.objects.create(name="Team Alpha")

        self.user1.team = self.team
        self.user1.save()
        self.user2.team = self.team
        self.user2.save()

    def test_serialization(self):
        serializer = TeamSerializer(instance=self.team)
        data = serializer.data
        self.assertEqual(data["name"], "Team Alpha")
        self.assertEqual(set(data["members_info"]), {"user1", "user2"})
        self.assertNotIn("members", data)

    def test_deserialization(self):
        data = {"name": "Team Beta", "members": [self.user1.id, self.user2.id]}
        serializer = TeamSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        team = serializer.save()
        self.assertEqual(team.name, "Team Beta")
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.team, team)
        self.assertEqual(self.user2.team, team)
