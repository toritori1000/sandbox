import os

# Implement tag
from taggit.managers import TaggableManager
# Replace native ImageField to enable image manipulation
from sorl.thumbnail import ImageField

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def save(self, *args, **kwargs):
        """
        Slugify title if slug field doesn't exist.
        IMPORTANT: doesn't check to see if slug is a dupe!
        """
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


# The settings for MEDIA_ROOT and MEDIA_URL come from the project settings
# but could be overridden in the model
# MEDIA_ROOT = '/django-home-dir/media/images/blog'
# MEDIA_URL = '/media'
class PostImage(models.Model):
    """Images for Blot Posts"""
    # allows for an image to be either stored in the MEDIA_ROOT path or
    # be a reference to an external URL to an image.
    image = models.ImageField(
        upload_to=os.path.join('images', 'blog'))
    title = models.CharField(max_length=255)
    legend = models.TextField(blank=True, null=True)
    description = models.TextField()
    external_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #
    # Display image in admin
    #
    def path(self):
        return os.path.join('/', settings.MEDIA_URL, 'images', 'blog',
                            os.path.basename(str(self.image)))

    def image_tag(self):
        """Config image display in admin"""
        # Fixed height
        return mark_safe(
            '<img src="{}" height="200" />'.format(self.path())
        )
    image_tag.short_description = 'Main Image'

    #
    # Second image
    #
    img2 = models.ImageField(
        upload_to=os.path.join('images', 'blog'), blank=True, null=True)
    img2_title = models.TextField(blank=True, null=True)
    legend2 = models.TextField(blank=True, null=True)
    img2_description = models.TextField(blank=True, null=True)
    img2_external_url = models.URLField(blank=True, null=True)
    img2_created_at = models.DateTimeField(auto_now_add=True, blank=True,
                                           null=True)

    def img2_path(self):
        return os.path.join('/', settings.MEDIA_URL, 'images', 'blog',
                            os.path.basename(str(self.img2)))

    # Display image in admin
    def img2_tag(self):
        return mark_safe(
            '<img src="{}" height="200"/>'.format(
                self.img2_path())
        )
    img2_tag.short_description = 'Second Image'

    #
    # Third image
    #
    img3 = models.ImageField(
        upload_to=os.path.join('images', 'blog'), blank=True, null=True)
    img3_title = models.TextField(blank=True, null=True)
    legend3 = models.TextField(blank=True, null=True)
    img3_description = models.TextField(blank=True, null=True)
    img3_external_url = models.URLField(blank=True, null=True)
    img3_created_at = models.DateTimeField(auto_now_add=True, blank=True,
                                           null=True)

    def img3_path(self):
        return os.path.join('/', settings.MEDIA_URL, 'images', 'blog',
                            os.path.basename(str(self.img3)))

    # Display image in admin
    def img3_tag(self):
        return mark_safe(
            '<img src="{}" height="200"/>'.format(
                self.img3_path())
        )
    img3_tag.short_description = 'Second Image'

    #
    # Fourth image
    #
    img4 = models.ImageField(
        upload_to=os.path.join('images', 'blog'), blank=True, null=True)
    legend4 = models.TextField(blank=True, null=True)
    img4_title = models.TextField(blank=True, null=True)
    img4_description = models.TextField(blank=True, null=True)
    img4_external_url = models.URLField(blank=True, null=True)
    img4_created_at = models.DateTimeField(auto_now_add=True, blank=True,
                                           null=True)

    def img4_path(self):
        return os.path.join('/', settings.MEDIA_URL, 'images', 'blog',
                            os.path.basename(str(self.img3)))

    # Display image in admin
    def img4_tag(self):
        return mark_safe(
            '<img src="{}" height="200"/>'.format(
                self.img4_path())
        )
    img4_tag.short_description = 'Second Image'

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # Set default value to 1, which corresponds to category "Other",
    # assuming the 1st row of Category table is defined as "Other".
    categories = models.ManyToManyField(Category, default=1)
    image_set = models.ForeignKey(PostImage, on_delete=models.CASCADE,
                                  blank=True, null=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['created_date']

    def save(self, *args, **kwargs):
        """
        Slugify title if slug field doesn't exist.
        IMPORTANT: doesn't check to see if slug is a dupe!
        """
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    item = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text
