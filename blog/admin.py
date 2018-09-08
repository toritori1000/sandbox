from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from blog.models import Post, Comment, Category, PostImage, EventDate

from sorl.thumbnail.admin import AdminImageMixin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'title', 'slug', 'text', 'image_set',
                           'tags', 'categories', 'event_date']}),
        ('Date Information', {'fields': ['published_date'],
                              'classes': ['collapse']})
    ]
    inlines = [CommentInline]


class PostImageAdmin(AdminImageMixin, admin.ModelAdmin):
    """Display image in admin"""
    # Explicitly reference fields to be shown, note image_tag is read-only.
    # The 'More images' are defined as open/collapsablei field sets
    fieldsets = (
        (None, {
            'fields': ('image', 'image_tag', 'title', 'legend', 'description',
                       'external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img2', 'img2_tag', 'img2_title', 'legend2',
                       'img2_description', 'img2_external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img3', 'img3_tag', 'img3_title', 'legend3',
                       'img3_description', 'img3_external_url')
        }),
        ('More images', {
            'classes': ('collapse', 'open'),
            'fields': ('img4', 'img4_tag', 'img4_title', 'legend4',
                       'img4_description', 'img4_external_url')
        }),
    )
    readonly_fields = ('image_tag', 'img2_tag', 'img3_tag', 'img4_tag')


class EventDateAdminForm(forms.ModelForm):
    class Meta:
        model = EventDate
        # __all_ or a list of the fields that you want to include in your form
        fields = '__all__'

    # This is the solution for the following error.
    # An "UNIQUE constraint failed: ..." error occurs related to unique fields.
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
            'fields': ('century', 'decade', 'year', 'month', 'day', 'date')
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
