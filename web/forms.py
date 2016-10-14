from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from core.models import Team, City, Athlete, Profile, Position, Match
from django.core.files import File
from varzeapro import settings
from django.db import transaction

class TeamForm(ModelForm):
    logo_file_name = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Team
        city = forms.ModelChoiceField(
            queryset=City.objects.all(),
            required=False
        )
        fields = ['name','city','foundation','president','logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'foundation': forms.DateInput(
                attrs={'class': 'form-control datepicker'}
            ),
            'city': forms.Select(attrs={'class': 'select2_single form-control select-city', 'tabindex': '-1'}),
            'president': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        logo_file_name = self.cleaned_data.get('logo_file_name', None)

        if logo_file_name:
            instance.logo = File(
                open(settings.MEDIA_TMP_DIR+logo_file_name),
                logo_file_name
            )

        if commit:
            instance.save()

        return instance

class AthleteForm(ModelForm):
    photo_file_name = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    email = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput({'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Athlete
        fields = ['position']
        position = forms.ModelChoiceField(
            queryset=Position.objects.all()
        )
        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, team_id, *args, **kwargs):
        self.team_id = team_id
        super(AthleteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AthleteForm, self).save(commit=False)
        photo_file_name = self.cleaned_data.get('photo_file_name', None)
        email = self.cleaned_data.get('email', None)
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        phone = self.cleaned_data.get('phone', None)

        with transaction.atomic():
            if not instance.id:
                user = User.objects.create(
                    username = email,
                    first_name = first_name,
                    last_name = last_name,
                    email = email
                )

                profile = Profile(
                    user = user,
                    phone = phone
                )

                if photo_file_name:
                    profile.photo = File(
                        open(settings.MEDIA_TMP_DIR+photo_file_name),
                        photo_file_name
                    )

                profile.save()

                instance.profile = profile
                instance.team_id = self.team_id
            else:
                profile = instance.profile

                if photo_file_name:
                    profile.photo = File(
                        open(settings.MEDIA_TMP_DIR+photo_file_name),
                        photo_file_name
                    )

                user = profile.user
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                profile.phone = phone
                profile.save()

            if commit:
                instance.save()

        return instance

class MatchForm(ModelForm):
    home = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'flat'}),
        required = False
    )

    class Meta:
        model = Match
        fields = ['arena', 'home_team', 'visitor_team', 'when']
        widgets = {
            'when': forms.DateInput(
                attrs={'class': 'form-control datetimepicker'}
            ),
            'arena': forms.Select(
                attrs={'class': 'form-control select2_single select-arena'}
            )
        }
