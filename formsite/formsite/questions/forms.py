from django import forms
from django.contrib.auth.models import User
from .models import Questions

class QuestionCreate(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('question','required','number','type')