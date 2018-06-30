from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text']}),
        ('Date Information', {'fields': ['published_date'], 'classes': ['collapse']})
    ]
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
