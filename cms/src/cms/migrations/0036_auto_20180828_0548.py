# Generated by Django 2.0.8 on 2018-08-28 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0040_page_draft_title'),
        ('cms', '0035_auto_20180827_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentindexpage',
            name='i18npage_ptr',
        ),
        migrations.DeleteModel(
            name='ContentIndexPage',
        ),
    ]