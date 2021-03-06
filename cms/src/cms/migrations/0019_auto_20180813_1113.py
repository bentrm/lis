# Generated by Django 2.0.8 on 2018-08-13 11:13

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('cms', '0018_auto_20180809_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('i18npage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.I18nPage')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'blockquote', 'link'])), ('image', wagtail.images.blocks.ImageChooserBlock())])),
                ('body_de', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'blockquote', 'link'])), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, default=[])),
                ('body_cs', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'blockquote', 'link'])), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, default=[])),
            ],
            options={
                'verbose_name': 'Blog page',
                'verbose_name_plural': 'Blog pages',
                'db_table': 'cms__content_pages',
            },
            bases=('cms.i18npage',),
        ),
        migrations.CreateModel(
            name='ContentIndexPage',
            fields=[
                ('i18npage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cms.I18nPage')),
            ],
            options={
                'verbose_name': 'Inhalt',
                'db_table': 'content_index',
            },
            bases=('cms.i18npage',),
        ),
        migrations.AddField(
            model_name='i18npage',
            name='alias_for_page',
            field=models.ForeignKey(blank=True, help_text='A temproary redirect target for this page. If set all incoming requests for this page will be redirected to this target page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aliases', to='wagtailcore.Page', verbose_name='Redirect target'),
        ),
    ]
