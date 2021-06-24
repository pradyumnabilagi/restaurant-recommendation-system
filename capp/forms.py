from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MenuForm(ModelForm):
    class Meta:
        model = menu
        fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
        #fields = UserCreationForm.Meta.fields + ('address',)
		fields = ['username', 'email', 'password1', 'password2']




