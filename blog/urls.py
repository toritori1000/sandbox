from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<tag_slug>', views.index, name="post_by_tag"),
    path('cat/<cat_slug>', views.index, name="post_by_cat"),
    path('post/<post_slug>', views.post_page, name='post_page'),
    path('post/search/', views.search, name='search'),
]
