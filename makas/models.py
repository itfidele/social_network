from django.db import models
import datetime
from django.db.models import Q
from django.utils import timezone
from django.contrib import admin
# Create your models here.
class Members(models.Model):

    def get_absolute_url(self):
        return reverse("dashboard", args={'photo': self.photo})

    def fullname(self):
        return self.firstname+" "+self.lastname

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
    biography = models.TextField(blank=True)
    friends=models.ManyToManyField('self',blank=True)
    

    def __str__(self):
        return self.firstname+" "+self.lastname

    full_name=property(fullname)

    def photo_available(self):
        if self.photo=='':
            return False
        else:
            return True
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    @property
    def number_of_friends(self):
        return self.friends.count

class Posts(models.Model):

    def postlike(self):
        resplike =PostLikes.objects.filter(post=self).count()
        return str(resplike)

    postcontent = models.TextField(blank=False)
    postviews = models.IntegerField(default=0)
    posttime = models.TimeField(
        auto_created=datetime.time, default=datetime.time)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    attachment = models.ImageField(
        'Post Attachment', blank=True, upload_to='post/')
    createdon = models.DateTimeField(auto_now=True, blank=True)
    likes=models.ManyToManyField(Members,blank=True,related_name='likes')

    def __str__(self):
        return self.postcontent

    def attachment_available(self):
        if self.attachment=='':
            return False
        else:
            return True

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comments(models.Model):
    comment = models.TextField(blank=False)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class PostLikes(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    createdon = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PostLike'
        verbose_name_plural = 'PostLikes'

class Friend(models.Model):
    friend_from=models.ForeignKey(Members,on_delete=models.CASCADE,related_name='friend_from')
    friend_to=models.ForeignKey(Members,on_delete=models.CASCADE,related_name='friend_to')
    friend_action=models.CharField(max_length=6,default='no')

    def __str__(self):
        return "friend from "+self.friend_from.username.upper()+" to "+self.friend_to.username.upper()
    
    def fromm(self):
        return friend_from

    frm=property(fromm)


