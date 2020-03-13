from django.contrib import admin
from django.urls import path
from . import views
from .views import MemberAPI,DetailMemberAPI


urlpatterns = [
    path('', views.index, name='index'),
    path('meapi',MemberAPI.as_view()),
    path('meapi/<int:pk>/',DetailMemberAPI.as_view()),
    path('register', views.register, name="register"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name='login'),
    path('post', views.post, name='new_post'),
    path('comment',views.comment,name='comment'),
    path('refreshComment',views.refreshComment,name='refreshComment'),
    path('postlike',views.like_post,name='postlike'),
    path('home-friend',views.friend_home,name='friends'),
    path('settings',views.settings,name='settings'),
    path('album',views.album,name='album'),
    path('addfriend',views.add_friend,name='addfriend'),
    path('confirmfriend',views.confirm_friend,name='confirmfriend'),
]
    