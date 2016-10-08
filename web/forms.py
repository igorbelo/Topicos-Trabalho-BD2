from django import forms
from django.forms import ModelForm
from core.models import Team, City

class TeamForm(ModelForm):
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
