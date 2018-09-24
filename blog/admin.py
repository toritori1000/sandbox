from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from blog.models import Post, Comment, Category, PostImage, EventDate, HomePost
# from blog.models import Post, Comment, Category, PostImage, EventDate

from sorl.thumbnail.admin import AdminImageMixin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'title', 'thumbnail_title', 'keywords',
                           'slug', 'text', 'image_set', 'tags', 'categories',
                           'event_date']}),
        ('Date Information', {'fields': ['published_date', 'created_date'],
                              'classes': ['collapse']})
    ]
    readonly_fields = ('created_date',)
    inlines = [CommentInline]


class HomePostForm(forms.ModelForm):

    class Meta:
        model = HomePost
        fields = '__all__'

    def clean(self):
        """
        Raise error if any feature_posts (many-to-many field) values the same
        as title_post.
        """
        header_post = self.cleaned_data.get('header_post')
        header_post_2 = self.cleaned_data.get('header_post_2')
        feature_posts = self.cleaned_data.get('feature_posts')

        for feature_post in feature_posts:
            if feature_post == header_post:
                raise ValidationError(
                    "The feature post needs to be different from "
                    "the selected title post: '{}'.".format(header_post))

            if feature_post == header_post_2:
                raise ValidationError(
                    "The feature post needs to be different from "
                    "the selected title post: '{}'.".format(header_post_2))


class HomePostAdmin(admin.ModelAdmin):
    form = HomePostForm

    fieldsets = [
        (None, {'fields': ['current', 'title', 'caption', 'description',
                           'alt_text', 'header_post', 'header_post_2',
                           'feature_posts']}),
        ('Date Information', {'fields': ['published_date', 'created_date'],
                              'classes': ['collapse']})
    ]
    readonly_fields = ('created_date',)

    def save_model(self, request, obj, form, change):
        # Reset 'current' field values of all other rows to 0
        for item in HomePost.objects.all():
            item.current = 0
            item.save()
        obj.save()


class PostImageAdmin(AdminImageMixin, admin.ModelAdmin):
    """Display image in admin"""
    # Explicitly reference fields to be shown, note image_tag is read-only.
    # The 'More images' are defined as open/collapsablei field sets
    fieldsets = (
        (None, {
            'fields': ('image', 'image_tag', 'title', 'legend', 'description',
                       'use_right_info', 'blockquote',
                       'external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img2', 'img2_tag', 'img2_title', 'img2_legend',
                       'img2_description', 'use_right_info',
                       'img2_blockquote', 'img2_external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img3', 'img3_tag', 'img3_title', 'img3_legend',
                       'img3_description', 'img3_use_right_info',
                       'img3_blockquote', 'img2_external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img4', 'img4_tag', 'img4_title', 'img4_legend',
                       'img4_description', 'img4_use_right_info',
                       'img4_blockquote', 'img2_external_url')
        }),
    )
    readonly_fields = ('image_tag', 'img2_tag', 'img3_tag', 'img4_tag')


class EventDateAdminForm(forms.ModelForm):
    class Meta:
        model = EventDate
        # __all_ or a list of the fields that you want to include in your form
        fields = '__all__'

    # This is the solution for the following unique fields related error.
    # "UNIQUE constraint failed: ..."
    # https: // code.djangoproject.com/ticket/12028
    #
    # Important! The function name 'clean_date' needs to match the variabl
    # name 'date' in the function.
    #
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if EventDate.objects.filter(date=date).exists():
            raise forms.ValidationError("This date value already exist.")

    """
    def clean_fields(self):
        if 1 == 1:
            raise ValidationError("VVVVQQQ")
    """


class EventDateAdmin(admin.ModelAdmin):
    form = EventDateAdminForm

    fieldsets = (
        (None, {
            'fields': ('century', 'decade', 'year', 'month', 'day', 'date',
                       'decade_by_five'
                       )
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('duration_decade', 'duration_year', 'duration_month',
                       'duration_day')
        }),
    )
    readonly_fields = ('date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(HomePost, HomePostAdmin)
