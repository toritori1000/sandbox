from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),

    # ATTN! include trailing slash. The default APPEND_SLASH=True in settings.
    path('', views.home, name='home'),
    path('blog/', views.home, name='blog'),
    path('index/', views.index, name='index'),
    path('index/post/<post_slug>/', views.post_page, name='post_page'),
    path('index/tag/<tag_slug>/', views.index, name="post_by_tag"),
    path('index/cat/<cat_slug>/', views.index, name="post_by_cat"),
    path('index/event/<event_year>/', views.index, name="post_by_event"),
    path('index/arch/<arch_date>/', views.index, name="post_by_arch"),
    path('post/search/', views.search, name='search'),

    path('aboutus/', views.aboutus, name='aboutus'),
    path('authors/', views.authors, name='authors'),
    path('archive/', views.archive, name='archive'),


]

# Example URLs
# http://localhost:8000/blog/index/post/post-example-2
# http://localhost:8000/blog/index/tag/tag3
# http://localhost:8000/blog/index/cat/infectious-diseases
# http://localhost:8000/blog/index/event/1950-1999
# http://localhost:8000/blog/index/arch/2018-09
# http://localhost:8000/blog/post/search/?q=vaccine
