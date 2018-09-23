import datetime
from functools import reduce
import operator
import os
import pprint
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from django.core.paginator import Paginator
from django.db.models.query import prefetch_related_objects
from django.db.models import Q
from blog.models import Post, Comment, Category, PostImage, EventDate, HomePost
from taggit.models import Tag


def home(request):

    # Get home posts
    home_post = HomePost.objects.filter(current=1)

    header_post_id = home_post[0].header_post_id
    header_post_2_id = home_post[0].header_post_2_id
    header_post = Post.objects.filter(id=header_post_id)
    header_post_2 = Post.objects.filter(id=header_post_2_id)
    feature_posts = home_post[0].feature_posts.all()

    # Get most recent 6 posts of each category
    # Note: prepend '-' to get last 6, then filip the order by reversed()
    recent_posts = reversed(Post.objects.all().order_by('-created_date')[0:6])

    # ATTN!!: header image needs to be a long image width > 300px
    context = {
        'home_post': home_post[0],
        'header_post': header_post[0],
        'header_post_2': header_post_2[0],
        'feature_posts': feature_posts,
        'recent_posts': recent_posts
    }

    # return HttpResponse(test)
    return render(request, 'blog/home.html', context)


def index(request,
          tag_slug=None, cat_slug=None, arch_date=None, event_year=None):
    #
    # ATTN!
    # The sidebar context items, including context['posts'] is populated
    # through genrate_sidebar().
    # The 'posts' value however might be replaced in specific page views,
    # such as post_page(), search().
    context = generate_sidebar_context(request,
                                       tag_slug, cat_slug, arch_date,
                                       event_year)

    return render(request, 'blog/index.html', context)


def post_page(request,
              post_slug, tag_slug=None, cat_slug=None, arch_date=None,
              event_year=None):

    ##################
    # For sidebar
    ##################
    # posts_context_dic = generate_sidebar_context(request, context,
    #                                             tag_slug, cat_slug,
    #                                             arch_date, event_year)
    # posts = posts_context_dic['posts']
    # context = posts_context_dic['context']
    context = generate_sidebar_context(request,
                                       tag_slug, cat_slug,
                                       arch_date, event_year)

    # Get a post by slug
    # http://localhost:8000/blog/post/post-example-2
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.all()
    tags = Tag.objects.all()

    image_obj = get_object_or_404(PostImage, id=post.image_set_id)

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

            # Add page specific items to context
            context['post'] = post
            context['comments'] = comments
            context['new_comments'] = comment

            return render(request, 'blog/post_page.html', context)
    else:

        context['post'] = post
        context['comments'] = comments
        context['image_url'] = image_obj.image
        context['image_obj'] = image_obj

        return render(request, 'blog/post_page.html', context)


def generate_sidebar_context(request,
                             tag_slug=None, cat_slug=None, arch_date=None,
                             event_year=None):
    """Utility function that handels sidebar context."""

    posts = Post.objects.all()
    context = {}

    # Tag search
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        context['tag'] = tag

    # Category search
    if cat_slug:
        cat_ids = Category.objects.filter(
            slug=cat_slug).values_list('id', flat=True)
        posts = posts.filter(categories__in=cat_ids)
        context['cat'] = cat_ids

        # cat_ids = get_object_or_404(
        #    Category, slug=cat_slug).values_list('id', flat=True)
        test = len(cat_ids)
        test = cat_slug

    # Archive search
    if arch_date:
        ym = arch_date.split("-")
        posts = Post.objects.filter(created_date__year=ym[0],
                                    created_date__month=ym[1])

    # Event year search
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

    # Pass filtered posts back to context 'posts'
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

    # return {'posts': posts, 'context': context}
    return context


def get_post_items(posts):
    """Utility function. Define display items for posts."""

    post_items = []
    for post in posts:
        post_url = reverse('post_page', kwargs={'post_slug': post.slug})
        post_item = {
            'title': post.title,
            'text': post.text,
            'keywords': post.keywords,
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

        # Append new reduce() for search fields
        """
        results = posts.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(text__icontains=q) for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(tags__name__icontains=q) for q in query_tokens)) |
        )
        """
        results = posts.filter(
            # title
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_tokens)) |
            # text
            reduce(operator.and_,
                   (Q(text__icontains=q) for q in query_tokens)) |
            # keywords
            reduce(operator.and_,
                   (Q(keywords__icontains=q) for q in query_tokens)) |
            # tags
            reduce(operator.and_,
                   (Q(tags__name__icontains=q) for q in query_tokens)) |
            # categories
            reduce(operator.and_,
                   (Q(categories__title__icontains=q) for q in query_tokens)) |

            # image title
            reduce(operator.and_,
                   (Q(image_set__title__icontains=q) for q in query_tokens)) |
            # image description
            reduce(operator.and_,
                   (Q(image_set__description__icontains=q)
                    for q in query_tokens)) |
            # image legend
            reduce(operator.and_,
                   (Q(image_set__legend__icontains=q) for q in query_tokens)) |

            # image 2
            reduce(operator.and_,
                   (Q(image_set__img2_title__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img2_description__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img2_legend__icontains=q)
                    for q in query_tokens)) |

            # image 3
            reduce(operator.and_,
                   (Q(image_set__img3_title__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img3_description__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img3_legend__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img4_title__icontains=q)
                    for q in query_tokens)) |

            # image 4
            reduce(operator.and_,
                   (Q(image_set__img4_description__icontains=q)
                    for q in query_tokens)) |
            reduce(operator.and_,
                   (Q(image_set__img4_legend__icontains=q)
                    for q in query_tokens))
        )

        # remove duplicates
        results = list(set(results))

        post_items = get_post_items(results)
    else:
        post_items = []

    test = len(results)
    test = len(post_items)

    ##################
    # For sidebar
    ##################
    # posts_context_dic = generate_sidebar_context(request, context)
    # posts = posts_context_dic['posts']
    # context = posts_context_dic['context']
    context = generate_sidebar_context(request)

    # Replace 'posts' and ddd page specific items to context
    context['posts'] = post_items
    context['query'] = query
    context['searchtest'] = test

    # context = {
    #    'posts': post_items,
    #    'query': query,
    #    'searchtest': test
    # }

    return render(request, 'blog/index.html', context)


def aboutus(request):
    mesg = 'The page is under construction.'
    # return HttpResponse(mesg)
    context = {
        'mesg': mesg,
    }
    return render(request, 'blog/aboutus.html', context)


def submit(request):
    mesg = 'The page is under construction.'
    context = {
        'mesg': mesg,
    }
    return render(request, 'blog/submit.html', context)


def contributors(request):
    mesg = 'The page is under construction.'
    context = {
        'mesg': mesg,
    }
    return render(request, 'blog/contributors.html', context)


def archive(request):
    mesg = 'The page is under construction.'
    context = {
        'mesg': mesg,
    }
    return render(request, 'blog/archive.html', context)
