# Generated by Django 2.0.8 on 2018-08-27 11:34

from django.db import migrations, models, connection
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


def insert_page_ptr(apps, schema_editor):
    BlogPage = apps.get_model("cms", "BlogPage")
    db_table = BlogPage._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {db_table} VALUES (3, '[]', '[]', '[]')")

def clear_ptr(apps, schema_editor):
    BlogPage = apps.get_model("cms", "BlogPage")
    db_table = BlogPage._meta.db_table

    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {db_table} where i18npage_ptr_id = 3")


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0034_auto_20180821_1348'),
    ]

    operations = [
        migrations.RunPython(insert_page_ptr, clear_ptr),
        migrations.RemoveField(
            model_name='homepage',
            name='i18npage_ptr',
        ),
        migrations.AddField(
            model_name='homepage',
            name='blogpage_ptr',
            field=models.OneToOneField(auto_created=True, default=3, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.BlogPage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'blockquote', 'link'])), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, default=[]),
        ),
    ]
