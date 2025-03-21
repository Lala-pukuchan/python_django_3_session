# tips/forms.py
from django import forms
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django import forms
from .models import Tip

class RegisterForm(forms.Form):
    username = forms.CharField(label="User name", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label="Password Confirm", widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password.")
            self.user = user  # Store for later use in the view
        return cleaned_data

# ModelForm can directly create and update model instances
class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']  # author and created_at will be automatically set
