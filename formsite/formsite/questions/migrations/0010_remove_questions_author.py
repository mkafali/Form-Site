# Generated by Django 5.0.3 on 2024-03-09 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_questions_belongs_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='author',
        ),
    ]