from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
import time
from questions.models import Questions

class Answer(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='question_of_answer')
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer_slug = models.SlugField(blank=True)
    answer = models.TextField(max_length=10000, blank=True)

    def __str__(self):
        return f"{self.answered_by.username}{self.question.slug}{self.answer_slug}"
    
    def save(self,*args,**kwargs):
        if not self.answer_slug:
            slug_var = str(time.time())
            while len(slug_var) < 17:
                slug_var += '0'
            self.answer_slug = slugify(slug_var)


        super().save(*args,**kwargs)