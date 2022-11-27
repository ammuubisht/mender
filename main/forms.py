from django.contrib.auth.models import User 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, ModelForm


from .models import *


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
    label= ('first_name'),
    widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'John'})
)
    last_name = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", 'username', 'email', 'password1']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        self.fields['first_name'].help_text = None
        self.fields['last_name'].help_text = None
        self.fields['email'].help_text = None