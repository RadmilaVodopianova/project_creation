from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path("post/<slug:post_slug>/", views.get_post, name="post"),
    path('post/', views.index, name='post_detail'),
    path('contact/', views.contact, name='contact'),
]
