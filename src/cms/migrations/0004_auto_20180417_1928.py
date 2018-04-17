# Generated by Django 2.0.2 on 2018-04-17 19:28

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20180417_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='memorialsitepage',
            name='detailed_description',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A detailed description of the memorial site and its significants to the referenced authors.', verbose_name='Detailed description'),
        ),
        migrations.AddField(
            model_name='memorialsitepage',
            name='detailed_description_cs',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A detailed description of the memorial site and its significants to the referenced authors.', verbose_name='Detailed description'),
        ),
        migrations.AddField(
            model_name='memorialsitepage',
            name='detailed_description_de',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A detailed description of the memorial site and its significants to the referenced authors.', verbose_name='Detailed description'),
        ),
    ]
