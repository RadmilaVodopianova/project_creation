from django.shortcuts import render
from django.utils import timezone
def dummy():
    return "func working"

def index(request):
    context = {
        "title": "Blog",
        "text": "HELLO WORLD!",
        "colors": ["red", "blue", "green"],
        "func": dummy,
        "today": timezone.now(),
    }
    return render(request, "blog/index.html", context)