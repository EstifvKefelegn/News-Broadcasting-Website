from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'email', 'password1', 'password2']

