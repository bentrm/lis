# Generated by Django 2.0.8 on 2018-09-13 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0038_auto_20180913_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorname',
            options={'verbose_name': 'Author name', 'verbose_name_plural': 'Author names'},
        ),
        migrations.AlterModelOptions(
            name='templocation',
            options={'verbose_name': 'Memorial site', 'verbose_name_plural': 'Memorial sites'},
        ),
        migrations.AlterModelTable(
            name='author',
            table='cms_author',
        ),
        migrations.AlterModelTable(
            name='authorindex',
            table='cms_authors',
        ),
        migrations.AlterModelTable(
            name='authorname',
            table='cms_author_name',
        ),
        migrations.AlterModelTable(
            name='homepage',
            table='cms_homepage',
        ),
        migrations.AlterModelTable(
            name='level1page',
            table='cms_level_1',
        ),
        migrations.AlterModelTable(
            name='level2page',
            table='cms_level_2',
        ),
        migrations.AlterModelTable(
            name='level3page',
            table='cms_level_3',
        ),
        migrations.AlterModelTable(
            name='location',
            table='cms_archive_location',
        ),
        migrations.AlterModelTable(
            name='locationindex',
            table='cms_locations',
        ),
        migrations.AlterModelTable(
            name='memorialsite',
            table='cms_archive_memorial_site',
        ),
        migrations.AlterModelTable(
            name='memorialsiteauthor',
            table='cms_archive_memorial_site_author',
        ),
        migrations.AlterModelTable(
            name='templocation',
            table='cms_memorial',
        ),
    ]
