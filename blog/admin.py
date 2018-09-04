from django.contrib import admin
from blog.models import Post, Comment, Category, PostImage
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


# Display image in admin
class PostImageAdmin(AdminImageMixin, admin.ModelAdmin):
    # explicitly reference fields to be shown, note image_tag is read-only
    # Open/collapsablei field sets
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


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostImage, PostImageAdmin)
