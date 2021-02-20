from django.contrib import admin
from .models import Post, PostCategory, Banner


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    ordering = ('status', '-publish')
    list_per_page = 20
    search_fields = ('title',)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_to', 'priority', 'pub_time')