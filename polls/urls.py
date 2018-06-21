from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
=======
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
>>>>>>> 57bcc81a0e338b9334b44927bcb42b5650b2c4df
    path('<int:question_id>/vote/', views.vote, name='vote'),
]