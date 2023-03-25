import operator
from functools import reduce

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin, TemplateView

from .models import Note, Category, Tag, Image
from .forms import *


# NOTE
class NoteList(ListView):
    model = Note
    queryset = Note.objects.all()

    def get(self, request, *args, **kwargs):
        super(NoteList, self).get(request, *args, **kwargs)
        if request.GET.get('tag'):
            tag = request.GET.get('tag')
            object_list = self.queryset.filter(tag=tag)
        elif request.GET.get('category'):
            category = request.GET.get('category')
            object_list = self.queryset.filter(Q(category=category) | Q(category__parent_category=category))
        elif request.GET.get('search'):
            query_set = request.GET.get('search').split(' ')
            query_result = reduce(operator.and_, ((
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__title__icontains=query) |
                    Q(tag__title__icontains=query)
            ) for query in query_set))
            object_list = self.queryset.filter(query_result)

        else:
            object_list = self.queryset
        context = self.get_context_data()
        context['object_list'] = object_list
        return self.render_to_response(context)


class NoteDetail(DetailView):
    model = Note
    template_name = 'note/note_detail.html'


class NoteCreate(CreateView):
    model = Note
    form_class = NoteImageForm
    success_url = reverse_lazy('note:note-list')
    extra_context = {'': Image.objects.none}

    def form_valid(self, form):
        image_set = self.request.FILES.getlist('images')
        with transaction.atomic():
            note = form.save()
            if len(image_set) == 1:
                img = image_set[0]
                image = Image.objects.create(image=img)
                image.title = f'{note.title}_{image.id}'
                note.image.add(image.id)
                note.save()
            else:
                for img in image_set:
                    image = Image.objects.create(image=img)
                    image.title = f'{note.title}_{image.id}'
                    note.image.add(image.id)
                    note.save()
        messages.add_message(self.request, messages.SUCCESS, f"Заметка добавлена")
        return redirect(self.success_url)


class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteImageForm
    second_form_class = TagFormSet
    template_name = 'note/note_update_form.html'

    def get(self, *args, **kwargs):
        formset_tag = TagFormSet(queryset=Tag.objects.none())
        context = {
            'tag_formset': formset_tag,
            'form': self.form_class,
            'object': self.get_object()
        }
        return self.render_to_response(context=context)

    def form_valid(self, form):
        image_set = self.request.FILES.getlist('images')
        tag_set = [int(tag) for tag in self.request.POST.getlist('tag')]

        with transaction.atomic():
            note = form.save(commit=False)
            old = note.tag.all()
            tag_set.extend(old)
            note.tag.set(tag_set)
            note.save()
            if len(image_set) == 1:
                img = image_set[0]
                image = Image.objects.create(image=img)
                image.title = f'{note.title}_{image.id}'
                note.image.add(image.id)
                note.save()
            else:
                for img in image_set:
                    image = Image.objects.create(image=img)
                    image.title = f'{note.title}_{image.id}'
                    note.image.add(image.id)
                    note.save()
        messages.add_message(self.request, messages.SUCCESS, f"Заметка обновлена")
        return redirect('note:note-list')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('note:note-list')

    def form_valid(self, form):
        success_url = self.success_url
        self.object.is_available = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class DeleteImage(DeleteView):
    model = Image

    def get(self, request, *args, **kwargs):
        note_id = kwargs['note_id']
        note = Note.objects.get(id=note_id)
        image_id = kwargs['image_id']
        image = Image.objects.get(id=image_id)
        if image in note.image.all():
            note.image.remove(image)
            Image.objects.filter(id=image.id).delete()
        note.save()
        messages.add_message(self.request, messages.INFO, f"Изображение успешно удалено")
        return redirect('note:note-edit', note.pk)


class DeleteTag(TemplateView):
    model = Tag

    def get(self, request, *args, **kwargs):
        note_id = kwargs['note_id']
        note = Note.objects.get(id=note_id)
        tag_id = kwargs['tag_id']
        tag = Tag.objects.get(id=tag_id)
        if tag in note.tag.all():
            note.tag.remove(tag)
        note.save()
        messages.add_message(self.request, messages.INFO, f"Тег {tag.title} откреплен от записи")
        return redirect('note:note-edit', note.pk)


# CATEGORY
class CategoryCreate(CreateView, ContextMixin):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('note:note-create')


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category


class CategoryUpdate(UpdateView):
    model = Category


class CategoryDelete(DeleteView):
    model = Category


# TAG
class TagCreate(CreateView):
    model = Tag
    template_name = 'tag/tag_form.html'
    form_class = TagForm
    success_url = reverse_lazy('note:note-list')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f"Тег добавлен")
        return super().form_valid(form)


class TagList(ListView):
    model = Tag
    template_name = 'tag/tag_list.html'


class TagDetail(DetailView):
    model = Tag


class TagUpdate(UpdateView):
    model = Tag


class TagDelete(DeleteView):
    model = Tag
