from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datetime/', views.current_datetime, name='datetime'),
]
