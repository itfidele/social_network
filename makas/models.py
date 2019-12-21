from django.db import models
import datetime
from django.contrib import admin
# Create your models here.


class Members(models.Model):
    GENDER_CHOICE = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    COUNTRIES = [
        ("RW", "Rwanda"),
        ("UG", "Uganda"),
        ("BU", "Burundi"),
        ("TZ", "Tanzania"),
    ]
    username = models.CharField(max_length=100, default='')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=250)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=3, choices=COUNTRIES)
    online = models.CharField(max_length=3, default='no')

    def __str__(self):
        return self.firstname


class PostImages(models.Model):
    attachment = models.FileField(upload_to='post/')


class Posts(models.Model):
    postcontent = models.TextField(blank=False)
    postviews = models.IntegerField(default=0)
    posttime = models.TimeField(auto_created=datetime.time, default=datetime.time)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    images = models.ManyToManyField(PostImages)


class Post(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    postimages = models.ForeignKey(PostImages, on_delete=models.CASCADE)


class AllPosts(admin.TabularInline):
    models = Post
    extra = 1


class AllPostImages(admin.ModelAdmin):
    inline = (Post,)


class AllPostsContent(admin.ModelAdmin):
    inline = (Post,)
