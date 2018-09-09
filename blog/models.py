import datetime
import os
import re

# Implement tag
from taggit.managers import TaggableManager
# Replace native ImageField to enable image manipulation
from sorl.thumbnail import ImageField

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


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


class EventDate(models.Model):

    CENTURIES = (
        (1700, '1700'),
        (1800, '1800'),
        (1900, '1900'),
        (2000, '2000'),
    )
    DECADES = (
        (10, '10'),
        (20, '20'),
        (30, '30'),
        (40, '40'),
        (50, '50'),
        (60, '60'),
        (70, '70'),
        (80, '80'),
        (90, '90'),
    )
    YEARS_IN_DECADE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
    )

    MONTHS_IN_YEAR = (
        (1, 'Jan'),
        (2, 'Feb'),
        (3, 'Mar'),
        (4, 'Apr'),
        (5, 'May'),
        (6, 'Jun'),
        (7, 'Jul'),
        (8, 'Aug'),
        (9, 'Sept'),
        (10, 'Oct'),
        (11, 'Nov'),
        (12, 'Dec'),
    )

    MONTHS = [(i, i) for i in range(1, 13)]

    DAYS = [(i, i) for i in range(1, 32)]

    century = models.IntegerField(choices=CENTURIES, default=2000)
    decade = models.IntegerField(default=0, choices=DECADES, null=True,
                                 blank=True)
    year = models.IntegerField(default=0, choices=YEARS_IN_DECADE, null=True,
                               blank=True)
    month = models.IntegerField(default=1, choices=MONTHS_IN_YEAR, null=True,
                                blank=True)
    day = models.IntegerField(default=1, choices=DAYS, null=True, blank=True)

    duration_decade = models.IntegerField(default=0, choices=DECADES,
                                          null=True, blank=True)
    duration_year = models.IntegerField(default=0, choices=YEARS_IN_DECADE,
                                        null=True, blank=True)
    duration_month = models.IntegerField(default=0, choices=MONTHS,
                                         null=True, blank=True)
    duration_day = models.IntegerField(default=0, choices=DAYS, null=True,
                                       blank=True)
    date = models.DateTimeField(blank=True, null=True)
    decade_by_five = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "Event Date"
        verbose_name_plural = "Event Dates"
        #
        # Note: need a 'clean_date' check in admin.py to deal with the error below.
        # "UNIQUE constraint failed: ..."
        #
        unique_together = ('century', 'decade', 'year', 'month', 'day')

    def none_to_zero(self):
        if self.decade is None:
            self.decade = 0
        if self.year is None:
            self.year = 0
        if self.month is None:
            self.month = 0
        if self.day is None:
            self.day = 0

    def compose_date(self):
        self.none_to_zero()
        years = self.century + self.decade + self.year

        # Format 2012-11-11 00:00:00
        event_datetime = datetime.datetime(year=years, month=self.month,
                                           day=self.day)
        # Format 1876 ---> 1850-1899
        decade_by_five = "{}-{}".format(str(years - years % 50),
                                        str(years - years % 50 + 49))
        return [event_datetime, decade_by_five]

    def clean(self):
        self.none_to_zero()

        years = int(self.century) + int(self.decade) + int(self.year)
        event_datetime = datetime.datetime(year=years, month=self.month,
                                           day=self.day)
        now = datetime.datetime.today()

        if event_datetime > now:
            raise ValidationError(
                "Input event date is later then now!  Input: {} --- Now: {}."
                .format(str(event_datetime), str(now), str(years),
                        str(self.century), str(self.decade),
                        str(self.year)))

    def get_db_prep_value(self, value, connection, prepared=False):
        value = models.Field.get_db_prep_value(
            self, value, connection, prepared)
        if value is not None:
            return connection.Database.Binary(self._dump(value))
        return value

    def save(self, *args, **kwargs):
        self.date = self.compose_date()[0]

        self.decade_by_five = self.compose_date()[1]
        super(EventDate, self).save(*args, **kwargs)

    def __str__(self):
        # Strip time
        # 2018-09-05 00:00:00+00:00 ---> 2018-09-05
        return re.sub(r'\s.*', '', str(self.date))


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
                                  blank=True, null=True,
                                  related_name='image_set')

    slug = models.SlugField(unique=True, null=True, blank=True)

    tags = TaggableManager()

    # Set default to id=3 (20th century)
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE,
                                   blank=True, null=True, default=3,
                                   related_name='post_event_date_set')

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
