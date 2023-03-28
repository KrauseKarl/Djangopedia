from django.db.models import Count

from .models import Category, Tag


def categories(request):
    return {'categories': Category.objects.annotate(pop=Count('sub_categories')).order_by('-pop')}


def tags(request):
    return {'tags': Tag.objects.order_by('title')}