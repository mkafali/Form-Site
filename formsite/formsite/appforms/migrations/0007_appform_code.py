# Generated by Django 5.0.3 on 2024-03-31 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appforms', '0006_appform_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='appform',
            name='code',
            field=models.TextField(blank=True),
        ),
    ]
