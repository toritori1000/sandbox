"""medsci URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.conf import settings
from django.conf.urls.static import static

# Note: in order to user blog:hme as below, app_name='blog' needs to be
# included in blog/urls.py
urlpatterns = [
    # path('', lambda r: HttpResponseRedirect(reverse('polls:home'))),

    path('', include('blog.urls')),  # NOTE: without $
    path('blog/', include('blog.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# This is required to display images in the 'media' directory
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# Note: setting home path with HttpResponseRedirect like following causes
# problem.
# path('', lambda r: HttpResponseRedirect(reverse('blog:home'))),
# The problem is due to the required app_name='blog' in app/urls.py,
# with which the error below is reported.
# 'post_page' is not a valid view function or pattern name.
# The error is related to the line below.
# post_url = reverse('post_page', kwargs={'post_slug': post.slug})
#
