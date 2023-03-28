import datetime
from django.db import models
from django.db.models import Count


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(default='', blank=True, verbose_name='описание')
    url = models.URLField(verbose_name='url', blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name='в наличии')

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='notes',
                                 verbose_name='категория')
    tag = models.ManyToManyField('Tag', max_length=100, blank=True, null=True, related_name='notes', verbose_name='тег')
    image = models.ManyToManyField('Image', blank=True, null=True, related_name='notes', verbose_name='изображение')

    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    objects = models.Manager()

    class Meta:
        db_table = 'notes'
        ordering = ('-updated',)
        verbose_name = 'заметка'
        verbose_name_plural = 'заметки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(Note, self).save(*args, **kwargs)

    @property
    def main_image(self):
        return self.image.first().image.url


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='название', unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    parent_category = models.ForeignKey('self', related_name='sub_categories', on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name='родительская категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    objects = models.Manager()

    class Meta:
        db_table = 'categories'
        ordering = ('title',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(Category, self).save(*args, **kwargs)

    @property
    def popular(self):
        return self.notes.annotate(Count('category__notes')).count()

class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='название', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='активный')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    objects = models.Manager()

    class Meta:
        db_table = 'tags'
        ordering = ('title',)
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(Tag, self).save(*args, **kwargs)


class Image(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name='название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата изменения')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', default='media/default/default_item.png', null=True,
                              blank=True, verbose_name='изображение')
    objects = models.Manager()

    class Meta:
        db_table = 'images'
        ordering = ['title']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return f'img - {self.pk}'
