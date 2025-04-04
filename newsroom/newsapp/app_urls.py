from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('privacy/',views.privacy_policy, name='privacy'),
    # path('weather/',views.weatherapi, name='weather'),
]