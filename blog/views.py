from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from taggit.models import Tag # ADD LIST OF POSTS WITH TAG

from .models import Post, Comment

# Create your views here.

def index(request, tag_slug=None):
    post_list = Post.objects.all()
    post_info_list = []
    context = {}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        context['tag']= tag

    for post in post_list:
        post_url = reverse('post_page', kwargs={'post_slug': post.slug})
        post_info = {'title': post.title, 'text': post.text, 'url': post_url}
        post_info_list.append(post_info)

        context['post_info_list'] = post_info_list

    return render(request, 'blog/index.html', context)


def post_page(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.all()

    if request.POST:
        comment = request.POST.get("comment")

        if not comment:
            return redirect('post_page')
        else:
            tbl_obj = Comment(item=post, text=comment, created_date=timezone.now(), published_date=timezone.now())
            tbl_obj.save()

            context = {
                'post': post,
                'comments': comments,
                'new_comment': comment,
            }

            return render(request, 'blog/post_page.html', context)

    else:
        context = {
            'post': post,
            'comments': comments,
        }

        return render(request, 'blog/post_page.html', context)
