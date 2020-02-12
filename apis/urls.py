from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('hac', views.index, name='apis'),
    path('yego', views.yego, name='yego'),
    path('webhook',views.webhook,name='webhook'),
]
    