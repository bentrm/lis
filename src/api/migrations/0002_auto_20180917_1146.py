# Generated by Django 2.0.8 on 2018-09-17 11:46

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(blank=True, default=api.models.generate_key, max_length=40, unique=True),
        ),
    ]
