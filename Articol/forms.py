from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.forms.models import ModelForm


from Articol.models import  Article


class ArticolForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'date_published', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




    def clean(self):
        cleaned_data = self.cleaned_data

        get_title = cleaned_data.get('title')




class ArticolUpdateForm(forms.ModelForm):
    class Meta:
        model =Article
        exclude = ['author', 'date_published', 'created_at', 'updated_at']

        widgets ={
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content'}),
        }


