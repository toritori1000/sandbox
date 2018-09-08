from django.contrib import admin
from blog.models import Post, Comment, Category, PostImage, EventDate
# from blog.models import Post, Comment, Category
from sorl.thumbnail.admin import AdminImageMixin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author', 'title', 'slug', 'text', 'image_set',
                           'tags', 'categories']}),
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


class EventDateAdmin(AdminImageMixin, admin.ModelAdmin):
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
