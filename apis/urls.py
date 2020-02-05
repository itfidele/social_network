from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dag.hf', views.index, name='index'),
    path('yego', views.yego, name='yego'),
    path('webhook',views.webhook,name='webhook'),
]
    