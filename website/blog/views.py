from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Post, Category, Tag, Profile
from .forms import (
    CommentForm, PostForm, SubscriberForm, RegisterForm,
    UserProfileForm, ProfileForm,
)


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


def index(request):
    posts = Post.objects.select_related(
        'category', 'user'
    ).prefetch_related('tags').all()

    tags = Tag.objects.all()
    category_id = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '')
    query = request.GET.get('q', '').strip()

    if category_id:
        try:
            category_pk = int(category_id)
        except ValueError:
            posts = posts.none()
        else:
            if 0 < category_pk < 2**63:
                posts = posts.filter(category_id=category_pk)
            else:
                posts = posts.none()

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator = Paginator(
        posts.distinct().order_by('-published_date', '-pk'),
        5,
    )
    page_obj = paginator.get_page(request.GET.get('page'))
    pagination_params = request.GET.copy()
    pagination_params.pop('page', None)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'page_numbers': paginator.get_elided_page_range(
            page_obj.number, on_each_side=1, on_ends=1,
        ),
        'pagination_query': pagination_params.urlencode(),
        'tags': tags,
        'selected_category': category_id,
        'selected_tag': tag_slug,
        'query': query,
    }

    context.update(get_categories())

    return render(request, 'blog/index.html', context)


@require_http_methods(['GET', 'POST'])
def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = post.comments.select_related('author').all()

    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                reverse('blog:login'),
            )

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('blog:post', post_slug=post.slug)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/post_detail.html', context)


@require_http_methods(['GET', 'POST'])
def subscribe(request):
    form = SubscriberForm(
        request.POST if request.method == 'POST' else None
    )

    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error(
                'email',
                'Ця електронна адреса вже підписана.',
            )
        else:
            messages.success(request, 'Ви успішно підписалися!')
            return redirect('blog:subscribe')

    context = {
        'form': form,
        'tags': Tag.objects.all(),
    }
    context.update(get_categories())

    return render(request, 'blog/subscribe.html', context)


def contact(request):
    context = {
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/contact.html', context)


def profile_detail(request, user_id):
    author = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.filter(user=author).first()
    posts = Post.objects.filter(user=author).select_related(
        'category', 'user'
    ).prefetch_related('tags')

    context = {
        'author': author,
        'profile': profile,
        'posts': posts,
        'tags': Tag.objects.all(),
    }
    context.update(get_categories())
    return render(request, 'blog/profile_detail.html', context)


@login_required(login_url='blog:login')
@require_http_methods(['GET', 'POST'])
def profile_edit(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile is None:
        profile = Profile(user=request.user)

    data = request.POST if request.method == 'POST' else None
    user_form = UserProfileForm(data, instance=request.user)
    profile_form = ProfileForm(data, instance=profile)

    if request.method == 'POST':
        user_valid = user_form.is_valid()
        profile_valid = profile_form.is_valid()
        if user_valid and profile_valid:
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            return redirect('blog:profile_detail', user_id=request.user.pk)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'tags': Tag.objects.all(),
    }
    context.update(get_categories())
    return render(request, 'blog/profile_edit.html', context)


@login_required(login_url='blog:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()

            return redirect('blog:index')
    else:
        form = PostForm()

    context = {
        'form': form,
        'tags': Tag.objects.all(),
    }
    context.update(get_categories())

    return render(request, 'blog/post_create.html', context)


@login_required(login_url='blog:login')
def post_update(request, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        user=request.user,
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            form.save()
            return redirect('blog:post', post_slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'post': post,
        'form': form,
        'tags': Tag.objects.all(),
    }
    context.update(get_categories())

    return render(request, 'blog/post_update.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})
