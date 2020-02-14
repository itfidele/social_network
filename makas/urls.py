from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name='login'),
    path('post', views.post, name='new_post'),
    path('comment',views.comment,name='comment'),
    path('refreshComment',views.refreshComment,name='refreshComment'),
    path('postlike',views.refreshLike,name='postlike')
]
    