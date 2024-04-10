from django import forms
from django.contrib.auth.models import User
from .models import AppForm
from questions.models import Questions

class FormCreate(forms.ModelForm):
    class Meta:
        model = AppForm
        fields = ('title',)

class FormQuestionCreate(forms.Form):
    form_title = forms.CharField(max_length=30)
    
    options = forms.CharField(max_length=1000, required=False)

