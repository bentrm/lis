# Generated by Django 2.0.8 on 2018-08-15 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0023_auto_20180815_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemedia',
            old_name='new_caption',
            new_name='caption',
        ),
        migrations.RenameField(
            model_name='imagemedia',
            old_name='new_caption_cs',
            new_name='caption_cs',
        ),
        migrations.RenameField(
            model_name='imagemedia',
            old_name='new_caption_de',
            new_name='caption_de',
        ),
    ]
