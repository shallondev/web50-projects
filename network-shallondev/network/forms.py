from django.forms import ModelForm
from django import forms

from .models import Post


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What is on your mind?'}),
        }
        required = {'content': True}  