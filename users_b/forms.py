""" All forms """
from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'email',
                'mobile_number', 'locale', 'redis_key']