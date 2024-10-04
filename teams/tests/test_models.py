from django.test import TestCase
from teams.models import Team
from django.core.exceptions import ValidationError


class TeamModelTest(TestCase):

    def setUp(self):
        self.team_name = "Team Alpha"
        self.team = Team.objects.create(name=self.team_name)

    def test_team_creation(self):
        self.assertEqual(self.team.name, self.team_name)
        self.assertTrue(isinstance(self.team, Team))
        self.assertEqual(str(self.team), self.team_name)

    def test_team_name_unique(self):
        with self.assertRaises(ValidationError):
            duplicate_team = Team(name=self.team_name)
            duplicate_team.full_clean()
            duplicate_team.save()

    def test_team_name_max_length(self):
        long_name = "A" * 101
        team = Team(name=long_name)
        with self.assertRaises(ValidationError):
            team.full_clean()

    def test_team_name_max_length_allowed(self):
        max_length_name = "A" * 100
        team = Team(name=max_length_name)
        team.full_clean()
        team.save()
        self.assertEqual(team.name, max_length_name)
