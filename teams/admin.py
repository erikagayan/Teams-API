from django.contrib import admin
from django import forms
from .models import Team
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple

User = get_user_model()


class TeamAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Members", is_stacked=False),
    )

    class Meta:
        model = Team
        fields = ["name", "members"]

    def __init__(self, *args, **kwargs):
        super(TeamAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["members"].initial = User.objects.filter(team=self.instance)

    def save(self, commit=True):
        team = super(TeamAdminForm, self).save(commit=False)
        if commit:
            team.save()
        if team.pk:
            team_members = self.cleaned_data["members"]
            # Set the team field for the selected users
            User.objects.filter(team=team).update(team=None)
            team_members.update(team=team)
        return team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ("name",)
    search_fields = ("name",)
