from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text',]


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']