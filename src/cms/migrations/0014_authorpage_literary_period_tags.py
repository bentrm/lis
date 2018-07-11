# Generated by Django 2.0.2 on 2018-07-06 12:22

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20180706_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorpage',
            name='literary_period_tags',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, db_table='cms_author_tag_literary_period', related_name='authors', to='cms.LiteraryPeriodTag'),
        ),
    ]
