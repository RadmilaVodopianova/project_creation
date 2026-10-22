from django.shortcuts import render
from django.utils import timezone


def dummy():
    return "func working!"


# Create your views here.
def index(request):
    context = {}
    return render(request, 'blog/index.html', context)


def get_post(request):
    context = {}
    return render(request, 'blog/post.html', context)


def contact(request):
    context = {}
    return render(request, 'blog/contact.html', context)