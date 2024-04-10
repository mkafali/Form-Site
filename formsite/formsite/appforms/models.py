from django.db import models
import random
import string
# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
import time
from questions.models import Questions

class AppForm(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=18, blank=True)
    title = models.CharField(max_length=30, blank=False)
    questions = models.ManyToManyField(Questions, blank=True)
    anonymous = models.BooleanField(default=False)
    filled_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='filled_by')
    code = models.CharField(blank=True, max_length=4)
    ask_code = models.BooleanField(default=False)
    form_code = models.CharField(blank=True,max_length=6)
    completed = models.BooleanField(default=False)
    is_changed = models.BooleanField(default=False)
    changed_time = models.CharField(blank=True, max_length=16)

    def __str__(self):
        return f"{self.author.username}{self.slug}"
    
    def save(self,*args,**kwargs):
        if not self.slug:
            slug_var = str(time.time())
            while len(slug_var) < 17:
                slug_var += '0'
            self.slug = slugify(slug_var)
        
        if not self.code:
            characters = string.ascii_lowercase + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(4))
            self.code = random_code
        
        if not self.form_code:
            characters = string.ascii_lowercase + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(6))
            self.form_code = random_code


        super().save(*args,**kwargs)


    class Meta:
        verbose_name_plural = "FORMS"
