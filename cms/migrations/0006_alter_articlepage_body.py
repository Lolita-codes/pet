# Generated by Django 4.1.6 on 2023-02-27 14:24

from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_alter_articlepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.fields.StreamField([('paragraph', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code', 'blockquote'])), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('html', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))], label='Code')), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(label='Image')), ('caption', wagtail.blocks.CharBlock(label='Caption', required=False)), ('float', wagtail.blocks.ChoiceBlock(choices=[('right', 'Right'), ('left', 'Left'), ('center', 'Center')], label='Float', required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], label='Size', required=False))])), ('video', wagtail.blocks.StructBlock([('video', wagtail.embeds.blocks.EmbedBlock(label='Video')), ('caption', wagtail.blocks.CharBlock(label='Caption', required=False)), ('float', wagtail.blocks.ChoiceBlock(choices=[('right', 'Right'), ('left', 'Left'), ('center', 'Center')], label='Float', required=False)), ('size', wagtail.blocks.ChoiceBlock(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], label='Size', required=False))]))], use_json_field=None),
        ),
    ]
