
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import Post, Category, Tag


def dummy():
    return "func working!"


def get_categories():
    categories = list(Category.objects.all())
    middle = len(categories) // 2

    first_half = categories[:middle]
    second_half = categories[middle:]

    return {
        'categories': first_half,
        'categories2': second_half,
    }


# Create your views here.
def index(request):
    posts = Post.objects.select_related(
        'category', 'user'
    ).prefetch_related('tags').all()

    tags = Tag.objects.all()

    category_slug = request.GET.get('category', '')
    tag_slug = request.GET.get('tag', '')
    query = request.GET.get('q', '').strip()

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    context = {
        'posts': posts.distinct(),
        'tags': tags,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'query': query,
    }

    context.update(get_categories())

    return render(request, 'blog/index.html', context)


def get_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    context = {
        'post': post,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/post.html', context)


def contact(request):
    context = {
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/contact.html', context)
