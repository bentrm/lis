# Generated by Django 2.0.8 on 2018-08-16 05:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('cms', '0027_auto_20180816_0519'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuthorPage',
            new_name='Author',
        ),
        migrations.RenameModel(
            old_name='AuthorPageName',
            new_name='AuthorName',
        ),
    ]
