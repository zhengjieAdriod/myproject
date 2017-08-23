from django import forms

from cases.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['image', 'worker', 'name', 'price', 'describe', 'scope', 'type']
