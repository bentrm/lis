# Generated by Django 2.0.8 on 2018-09-13 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0039_auto_20180913_1031'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='documentmedia',
            table='cms_document',
        ),
        migrations.AlterModelTable(
            name='imagemedia',
            table='cms_image',
        ),
        migrations.AlterModelTable(
            name='imagemediarendition',
            table='cms_image_rendition',
        ),
    ]
