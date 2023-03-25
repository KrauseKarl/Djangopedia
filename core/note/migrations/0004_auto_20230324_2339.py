# Generated by Django 3.2.4 on 2023-03-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_auto_20230323_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='note',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='note',
            name='image',
            field=models.ManyToManyField(related_name='notes', to='note.Image', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='note',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]