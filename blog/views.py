from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from taggit.models import Tag # ADD LIST OF POSTS WITH TAG

from .models import Post, Comment

from functools import reduce
import operator
from django.db.models import Q

def index(request, tag_slug=None):
    posts = Post.objects.all()
    context = {}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context['tag'] = tag

    post_items = get_post_items(posts)
    context['posts'] = post_items

    return render(request, 'blog/index.html', context)


def get_post_items(posts):
    """Build a list of display items given a list of post objects."""
    post_items = []
    for post in posts:
        post_url = reverse('post_page', kwargs={'post_slug': post.slug})
        post_item = {'title': post.title, 'text': post.text, 'url': post_url}
        post_items.append(post_item)

    return post_items


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


def search(request):
    """Filter posts text fields by search input."""

    query = request.GET.get('q')

    if query:
        posts = Post.objects.all().order_by("title")

        # Search all query words in the blog content, split the query into separate words.
        query_tokens = query.split()
        # Use reduce() to iterate through each post and filter() and operator() to achieve the
        # SQL query similar to the following.
        # SELECT * FROM blog_table WHERE content LIKE '%first_word%'
        # AND content LIKE '%second_word%' AND content LIKE '%third_word%'
        results = posts.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(text__icontains=q) for q in query_tokens))
        )

        post_items = get_post_items(results)
    else:
        post_items = []

    context = {
        'posts': post_items,
        'query': query
    }
    return render(request, 'blog/index.html', context)
    #test = context['posts']
    #return HttpResponse(test)
