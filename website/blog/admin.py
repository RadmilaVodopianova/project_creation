from django.contrib import admin

from .models import Post, Category, Tag, Profile, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "user",
        "published_date",
        "content_length",
        "slug",
    ]
    search_fields = ["title", "content"]
    list_filter = ["category", "published_date"]
    filter_horizontal = ["tags"]
    ordering = ["-published_date"]
    list_per_page = 10

    @admin.display(description="Довжина тексту")
    def content_length(self, obj):
        return len(obj.content)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "birth_date"]
    search_fields = ["user__username", "city"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'post__title')