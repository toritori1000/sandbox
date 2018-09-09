from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<post_slug>', views.post_page, name='post_page'),
    path('tag/<tag_slug>', views.index, name="post_by_tag"),
    path('cat/<cat_slug>', views.index, name="post_by_cat"),
    path('arch/<arch_date>', views.index, name="post_by_arch"),
    path('event/<event_year>', views.index, name="post_by_event"),
    path('post/search/', views.search, name='search'),
]
