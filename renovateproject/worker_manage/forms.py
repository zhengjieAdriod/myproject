from django import forms

from cases.models import Service, SchemeInService


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['image', 'worker', 'name', 'price', 'describe', 'scope', 'type']


class SchemeInServiceForm(forms.ModelForm):
    class Meta:
        model = SchemeInService
        fields = ['image', 'Service', 'name', 'price', 'describe']

    pass


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
