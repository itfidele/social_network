from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
# Create your models here.


class Members(models.Model):

    def get_absolute_url(self):
        return reverse("dashboard", args={'photo': self.photo})

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
    dateofbirth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        'Profile Picture', blank=True, upload_to='users/')
    created = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return self.firstname+" "+self.lastname

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    



class Posts(models.Model):
    postcontent = models.TextField(blank=False)
    postviews = models.IntegerField(default=0)
    posttime = models.TimeField(
        auto_created=datetime.time, default=datetime.time)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    attachment = models.ImageField(
        'Post Attachment', blank=True, upload_to='post/')
    createdon=models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return self.postcontent
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comments(models.Model):
    comment=models.TextField(blank=False)
    user=models.ForeignKey(Members,on_delete=models.CASCADE)
    createdon=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.comment

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class PostLikes(models.Model):
    like=models.IntegerField()
    user=models.ForeignKey(Members,on_delete=models.CASCADE)
    createdon=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PostLike'
        verbose_name_plural = 'PostLikes'