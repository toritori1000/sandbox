from functools import reduce
import operator
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone


from django.core.paginator import Paginator
from django.db.models.query import prefetch_related_objects
from django.db.models import Q
from blog.models import Post, Comment, Category, PostImage
from taggit.models import Tag

import pprint


def index(request, tag_slug=None, cat_slug=None):
    posts = Post.objects.all()
    context = {}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context['tag'] = tag

    if cat_slug:
        cat_ids = Category.objects.filter(
            slug=cat_slug).values_list('id', flat=True)
        posts = posts.filter(category_id__in=cat_ids)
        context['cat'] = cat_ids

    tags = Tag.objects.all()
    post_items = get_post_items(posts)
    context['posts'] = post_items

    # For sidebar
    context['tags'] = tags
    context['categories'] = Category.objects.all()

    # Build absolute url such as below for side-pan category link.
    # http://localhost:8000/blog/tag/
    # Note: The problem of relative url created by the href in templaste below
    # <a href = "{{ test }}{{ tag.slug }}" ...>
    # is that the tag link only works from blog base page. The link url is no
    # longer correct on the secondary page such as below.
    # http://localhost:8000/blog/tag/tag1/tag/tag2
    context['tag_base_url'] = os.path.join(request.build_absolute_uri(
        reverse('index')), 'tag/')
    context['cat_base_url'] = os.path.join(request.build_absolute_uri(
        reverse('index')), 'cat/')

    context['test'] = os.path.join(request.build_absolute_uri(
        reverse('index')), 'cat/')

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
    tags = Tag.objects.all()

    image_obj = get_object_or_404(PostImage, id=1)
    image_obj_2 = get_object_or_404(PostImage, id=2)

    if request.POST:
        comment = request.POST.get("comment")

        if not comment:
            return redirect('post_page')
        else:
            tbl_obj = Comment(item=post, text=comment,
                              created_date=timezone.now(),
                              published_date=timezone.now())
            tbl_obj.save()

            # add respective tags to the post as an attribute
            match_tags = tags.filter(id=post.pk)
            setattr(post, 'tags', match_tags)

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
            'image_url': image_obj.image,
            'image_obj': image_obj,
            'image_obj_2': image_obj_2
        }

        # For sidebar
        context['tags'] = tags
        context['categories'] = Category.objects.all()

        return render(request, 'blog/post_page.html', context)


def search(request):
    """Filter posts text fields by search input."""

    query = request.GET.get('q')

    if query:
        posts = Post.objects.all().order_by("title")

        # Search all query words in the blog content, split the query into
        # separate words.
        query_tokens = query.split()
        # Use reduce() to iterate through each post and filter() and operator()
        # to achieve the SQL query similar to the following.
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
    # test = context['posts']
    # return HttpResponse(test)
