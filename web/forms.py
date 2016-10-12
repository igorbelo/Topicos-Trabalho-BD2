from django import forms
from django.forms import ModelForm
from core.models import Team, City
from django.core.files import File
from varzeapro import settings

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
            'city': forms.Select(attrs={'class': 'select2_single form-control', 'tabindex': '-1'}),
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
