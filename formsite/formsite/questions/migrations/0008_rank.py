# Generated by Django 5.0.3 on 2024-03-08 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_multichoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='questions.questions')),
            ],
        ),
    ]
