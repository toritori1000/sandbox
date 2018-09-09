import datetime
from functools import reduce
import operator
import os
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone


from django.core.paginator import Paginator
from django.db.models.query import prefetch_related_objects
from django.db.models import Q
from blog.models import Post, Comment, Category, PostImage, EventDate
from taggit.models import Tag

import pprint


def index(request,
          tag_slug=None, cat_slug=None, arch_date=None, event_year=None):

    context = {}
    posts_context_dic = generate_sidebar_context(request, context,
                                                 tag_slug, cat_slug, arch_date,
                                                 event_year)
    posts = posts_context_dic['posts']
    context = posts_context_dic['context']

    return render(request, 'blog/index.html', context)


def post_page(request,
              post_slug, tag_slug=None, cat_slug=None, arch_date=None,
              event_year=None):

    # Get a post by slug
    # http://localhost:8000/blog/post/post-example-2
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.all()
    tags = Tag.objects.all()

    image_obj = get_object_or_404(PostImage, id=post.image_set_id)

    test = "WWWQQQ"
    test = post.image_set_id

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
        }

        ##################
        # For sidebar
        ##################
        posts_context_dic = generate_sidebar_context(request, context,
                                                     tag_slug, cat_slug,
                                                     arch_date, event_year)
        posts = posts_context_dic['posts']
        context = posts_context_dic['context']
        #context['tags'] = tags
        #context['categories'] = Category.objects.all()
        #context['test'] = test

        return render(request, 'blog/post_page.html', context)


def generate_sidebar_context(request, context,
                             tag_slug, cat_slug, arch_date, event_year):
    """Utility function that handels sidebar context."""

    posts = Post.objects.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context['tag'] = tag

    if cat_slug:
        cat_ids = Category.objects.filter(
            slug=cat_slug).values_list('id', flat=True)
        posts = posts.filter(id__in=cat_ids)
        context['cat'] = cat_ids

    if arch_date:
        ym = arch_date.split("-")
        posts = Post.objects.filter(created_date__year=ym[0],
                                    created_date__month=ym[1])

    if event_year:
        event_ids = EventDate.objects.filter(
            decade_by_five=event_year).values_list('id', flat=True)
        posts = posts.filter(event_date_id__in=event_ids)
        test = posts
        context['event'] = event_ids

    #####################
    # For sidebar
    #####################
    #
    # Not to use tags = Tag.objects.all() to get only tags that has Post assoc
    tags = Post.tags.all()
    post_items = get_post_items(posts)
    context['posts'] = post_items

    context['tags'] = tags
    context['categories'] = Category.objects.all()
    # Archive by year-month
    qs = Post.objects.extra(select={
        'year': "strftime('%%Y',created_date)",
        'month': "strftime('%Y-%m', created_date)", }).values(
        'year', 'month')
    # Get distinct year-month in the set
    ym_set = []
    for item in qs:
        ym_set.append(item['month'])
    context['post_year_month_set'] = list(set(ym_set))

    #
    # ### Event by Years ###
    #
    # Reverse ForeignKey relationship
    # Note: 'post_event_date_set' is defined in model Post
    qs = EventDate.objects.prefetch_related(
        'post_event_date_set').all()
    # Get distinct decade_by_five in the set
    post_event_ids = Post.objects.all().values_list('event_date_id', flat=True)
    decade_set = []

    for item in qs:
        # Include only the ones having assoc with post
        if item.id in post_event_ids:
            decade_set.append(item.decade_by_five)
    # Keep only unique values
    context['events'] = list(set(decade_set))

    #
    # ### Build absolute url ###
    #
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
    context['arch_base_url'] = os.path.join(request.build_absolute_uri(
        reverse('index')), 'arch/')
    context['event_base_url'] = os.path.join(request.build_absolute_uri(
        reverse('index')), 'event/')
    # context['test'] = os.path.join(request.build_absolute_uri(
    #    reverse('index')), 'cat/')

    return {'posts': posts, 'context': context}


def get_post_items(posts):
    """Utility function. Builds a list of display items given a list of
    post objects."""

    post_items = []
    for post in posts:
        post_url = reverse('post_page', kwargs={'post_slug': post.slug})
        post_item = {
            'title': post.title,
            'text': post.text,
            'url': post_url,
            # many-to-many field
            'categories': post.categories.all(),
            # foreign-key field
            'image_set': post.image_set,
            'event_date': post.event_date,
        }
        post_items.append(post_item)

    return post_items


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
