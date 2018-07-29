from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<tag_slug>', views.index, name="posts_by_tag"),
    path('post/<post_slug>', views.post_page, name='post_page'),
]
