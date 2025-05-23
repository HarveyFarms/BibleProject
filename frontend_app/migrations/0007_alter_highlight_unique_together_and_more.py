# Generated by Django 5.2 on 2025-04-24 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_app', '0006_alter_bibleverse_options_alter_verse_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='highlight',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='highlight',
            name='group',
        ),
        migrations.RemoveField(
            model_name='versecomment',
            name='group',
        ),
        migrations.RemoveField(
            model_name='versecomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Verse',
        ),
        migrations.DeleteModel(
            name='Highlight',
        ),
        migrations.DeleteModel(
            name='VerseComment',
        ),
    ]
