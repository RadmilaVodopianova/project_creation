from django.urls import path
from  . import views

app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('post/',views.get_post,name='post'),
    path("contact/", views.contact, name="contact"),
]