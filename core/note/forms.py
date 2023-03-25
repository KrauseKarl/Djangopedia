from django import forms
from django.forms import modelformset_factory

from .models import Note, Category, Tag, Image


class NoteForm(forms.ModelForm):
    title = forms.CharField(label='название', error_messages={'required': 'Это поле является обязательным.'})
    url = forms.URLField(error_messages={'required': 'Это поле является обязательным.'}, required=False)

    class Meta:
        model = Note
        fields = ('title',
                  'description',
                  'url',
                  'is_available',
                  'category', 'tag',
                  )


class NoteImageForm(NoteForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Изображения',
                              required=False)
    tags = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Изображения',
                            required=False)

    class Meta(NoteForm.Meta):
        fields = NoteForm.Meta.fields + ('images',)


TagFormSet = modelformset_factory(
    Tag,
    fields=("title",),
    extra=1
)


class CategoryForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': 'Это поле является обязательным.',
                                            'unique': 'Этот тег уже существует.', })

    class Meta:
        model = Category
        fields = ('title',
                  'description',
                  'parent_category',
                  )


class TagForm(forms.ModelForm):
    title = forms.CharField(error_messages={'required': 'Это поле является обязательным.',
                                            'unique': 'Этот тег уже существует.', })

    class Meta:
        model = Tag
        fields = ('title',)
