# Generated by Django 3.2.4 on 2023-03-25 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0004_auto_20230324_2339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ('updated',), 'verbose_name': 'заметка', 'verbose_name_plural': 'заметки'},
        ),
    ]
