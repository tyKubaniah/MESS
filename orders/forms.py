from django import forms
from django.contrib.auth.models import User
from .models import OfficerProfile

class OfficerSignUpForm(forms.ModelForm):
    service_number = forms.CharField(max_length=30, required=True, label="Service Number")
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Second Name")
    rank = forms.ChoiceField(choices=OfficerProfile.RANK_CHOICES, required=True, label="Current Rank")
    office_location = forms.CharField(max_length=100, required=True, label="Assigned Office/Base Location")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    class Meta:
        model = User
        fields = ['service_number', 'first_name', 'last_name', 'rank', 'office_location', 'password']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['service_number'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        OfficerProfile.objects.create(
            user=user,
            service_number=self.cleaned_data['service_number'],
            rank=self.cleaned_data['rank'],
            office_location=self.cleaned_data['office_location']
        )
        return user

class OfficeUpdateForm(forms.ModelForm):
    class Meta:
        model = OfficerProfile
        fields = ['office_location']