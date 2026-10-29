from django.contrib import admin

from .models import Category, Post, Profile, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "user",
        "published_date",
        "content_length",
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
    list_display = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "birth_date"]
    search_fields = ["user__username", "city"]