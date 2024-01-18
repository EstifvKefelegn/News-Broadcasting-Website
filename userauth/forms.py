from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import JournalistProfile


class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'email', 'password1', 'password2']

class JouranlistAcceptance(forms.ModelForm):
    class Meta:
        model = JournalistProfile
        fields = ['can_publish']