# Generated by Django 2.0.2 on 2018-05-21 15:35

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20180521_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level2page',
            name='biography',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text='Eine Kennung, welche es erlaubt die Fußnote im Abschnitt in der Form [Kennung] zu referenzieren.', label='Kennung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='Biography', verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='literaryperiodpage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A general description of the literary period and its significance.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='literaryperiodpage',
            name='description_cs',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A general description of the literary period and its significance.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='literaryperiodpage',
            name='description_de',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A general description of the literary period and its significance.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='address',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='The postal address of the location if any.', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='address_cs',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='The postal address of the location if any.', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='address_de',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='The postal address of the location if any.', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='directions',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A short description of directions to find the location.', verbose_name='How to get there'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='directions_cs',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A short description of directions to find the location.', verbose_name='How to get there'),
        ),
        migrations.AlterField(
            model_name='locationpage',
            name='directions_de',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='A short description of directions to find the location.', verbose_name='How to get there'),
        ),
    ]
