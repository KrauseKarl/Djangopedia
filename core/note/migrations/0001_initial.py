# Generated by Django 3.1 on 2023-03-22 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_categories', to='note.category', verbose_name='родительская категория')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'db_table': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='название')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'db_table': 'tags',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='название')),
                ('description', models.TextField(blank=True, default='', verbose_name='описание')),
                ('url', models.URLField(verbose_name='url')),
                ('is_available', models.BooleanField(default=False, verbose_name='в наличии')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='note.category', verbose_name='категория')),
                ('tag', models.ManyToManyField(blank=True, max_length=50, related_name='notes', to='note.Tag', verbose_name='тег')),
            ],
            options={
                'verbose_name': 'заметка',
                'verbose_name_plural': 'заметки',
                'db_table': 'notes',
                'ordering': ('title',),
            },
        ),
    ]