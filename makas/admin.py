from django.contrib import admin
from .models import Members, PostImages, AllPostImages, Posts, AllPostsContent

# Register your models here.

admin.site.register(Members)
admin.site.register(PostImages, AllPostImages)
admin.site.register(Posts, AllPostsContent)
