# Generated by Django 2.0.2 on 2018-04-28 17:27

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20180427_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='level2page',
            name='connections',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Connections'),
        ),
        migrations.AddField(
            model_name='level2page',
            name='connections_cs',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Connections'),
        ),
        migrations.AddField(
            model_name='level2page',
            name='connections_de',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Connections'),
        ),
        migrations.AddField(
            model_name='level2page',
            name='full_texts',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Full texts'),
        ),
        migrations.AddField(
            model_name='level2page',
            name='full_texts_cs',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Full texts'),
        ),
        migrations.AddField(
            model_name='level2page',
            name='full_texts_de',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='TODO', verbose_name='Full texts'),
        ),
        migrations.AlterField(
            model_name='level2page',
            name='reception',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='A more in-depth description for interested users on how the author has been received.', verbose_name='Reception'),
        ),
        migrations.AlterField(
            model_name='level2page',
            name='reception_cs',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='A more in-depth description for interested users on how the author has been received.', verbose_name='Reception'),
        ),
        migrations.AlterField(
            model_name='level2page',
            name='reception_de',
            field=wagtail.core.fields.StreamField((('paragraph', wagtail.core.blocks.StructBlock((('heading', wagtail.core.blocks.CharBlock(help_text='Eine optionale Überschrift um besonders umfassende Textinhalte weiter zu strukturieren.', label='Optionale Überschrift', required=False)), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), default=[], help_text='Bilder die nahe des eigentlichen Textinhalts des Abschnitts platziert werden sollen.', label='Bilder')), ('content', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'sup', 'ol', 'ul', 'hr', 'link', 'blockquote'], help_text='Der eigentliche Textinhalt des Abschnitts.', label='Inhalt', required=True)), ('footnotes', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('tag', wagtail.core.blocks.CharBlock(help_text="A tag that allows to link the footnote with the paragraphs text content in the form '[tag]'.", label='Kennzeichnung', required=False)), ('footnote', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'strikethrough', 'link'], help_text='Zitate, Kommentare und Referenzierungen', label='Fußnote')))), default=[], help_text='Optionale Fußnoten zum Textinhalt.', label='Fußnoten')), ('editor', wagtail.core.blocks.CharBlock(help_text='Der Autor oder Übersetzer, die Autorin oder Übersetzerin des Textinhalts.', label='Editor', required=True))))),), blank=True, help_text='A more in-depth description for interested users on how the author has been received.', verbose_name='Reception'),
        ),
    ]
