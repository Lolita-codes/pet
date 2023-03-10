# Generated by Django 4.1.6 on 2023-03-07 19:47

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('cms', '0012_alter_theme_locale_alter_theme_translation_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, help_text='Unique identifier of menu. Will be populated automatically from title of menu. Change only if needed.', populate_from='title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(help_text='Title of menu item that will be displayed', max_length=50)),
                ('link_url', models.CharField(blank=True, help_text='URL to link to, e.g. /accounts/signup (no language prefix, LEAVE BLANK if you want to link to a page instead of a URL)', max_length=500, null=True)),
                ('title_of_submenu', models.CharField(blank=True, help_text='Title of submenu (LEAVE BLANK if there is no custom submenu)', max_length=50, null=True)),
                ('show_when', models.CharField(choices=[('always', 'Always'), ('logged_in', 'When logged in'), ('not_logged_in', 'When not logged in')], default='always', max_length=15)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('link_page', models.ForeignKey(blank=True, help_text='Page to link to (LEAVE BLANK if you want to link to a URL instead)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.page')),
                ('menu', modelcluster.fields.ParentalKey(help_text='Menu to which this item belongs', on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='cms.menu')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
