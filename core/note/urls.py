from django.urls import path

from .views import *


app_name = 'note'

urlpatterns = [
    # NOTE
    path('', NoteList.as_view(), name='note-list'),
    path('create/', NoteCreate.as_view(), name='note-create'),
    path('<int:pk>', NoteDetail.as_view(), name='note-detail'),
    path('<int:pk>/edit/', NoteUpdate.as_view(), name='note-edit'),
    path('<int:pk>/remove/', NoteDelete.as_view(), name='note-remove'),
    path('<int:note_id>/remove/<int:image_id>/delete_image', DeleteImage.as_view(), name='note-remove-image'),
    path('<int:note_id>/remove/<int:tag_id>/delete_tag', DeleteTag.as_view(), name='note-remove-tag'),
    # CATEGORY

    path('category/list/', CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/detail/', CategoryDetail.as_view(), name='category-detail'),
    path('category/<int:pk>/edit/', CategoryUpdate.as_view(), name='category-edit'),
    path('category/create/', CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/remove/', CategoryDelete.as_view(), name='category-remove'),
    # TAG
    path('tag/create/', TagCreate.as_view(), name='tag-create'),
    path('tag/list/', TagList.as_view(), name='tag-list'),
    path('tag/edit/<int:pk>/', TagDetail.as_view(), name='tag-detail'),
    path('tag/edit/<int:pk>/', TagUpdate.as_view(), name='tag-edit'),
    path('tag/remove/<int:pk>/', TagDelete.as_view(), name='tag-remove'),

]
