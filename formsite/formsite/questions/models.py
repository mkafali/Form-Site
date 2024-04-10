from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
import time


# Create your models here.
class Questions(models.Model):
    belongs_to = models.ForeignKey('appforms.AppForm', on_delete=models.CASCADE, related_name='belongs_to', default=None)
    question = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(max_length=18, blank=True)
    number = models.IntegerField()
    question_types = (
    ("Optional", "Optional"),
    ("MultiChoices", "Multi Choices"),
    ("OpenEnded", "Open Ended"),
    ("Rank", "Rank"),
    )

    type = models.CharField(max_length=12,choices=question_types,default="OpenEnded")
    options = models.CharField(max_length=1000, blank=True)
    required = models.BooleanField(default=True)
    answers = models.ManyToManyField('answers.Answer', blank=True)

    def __str__(self):
        return f"{self.belongs_to.author.username}{self.slug}"
    
    def save(self,*args,**kwargs):
        if not self.slug:
            slug_var = str(time.time())
            while len(slug_var) < 17:
                slug_var += '0'
            self.slug = slugify(slug_var)


        super().save(*args,**kwargs)
        

    class Meta:
        verbose_name_plural = "Questions"
