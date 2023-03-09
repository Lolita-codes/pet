# Generated by Django 4.1.6 on 2023-02-27 17:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('cms', '0011_auto_20230227_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='locale',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.locale'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='translation_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='theme',
            unique_together={('translation_key', 'locale')},
        ),
    ]