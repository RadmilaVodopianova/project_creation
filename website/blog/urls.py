from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path("post/<slug:post_slug>/", views.post_detail, name="post"),
    path('post/', views.index, name='post_detail'),
    path('contact/', views.contact, name='contact'),
    path('profile/<int:user_id>/',views.profile_detail,name='profile_detail',),
]
