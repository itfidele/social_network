from django.contrib import admin
from .models import Members, Posts

# Register your models here.
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display=['postcontent','postviews','posttime','user','createdon']
    list_filter=['posttime']
    date_hierarchy='createdon'
    search_fields=['postcontent','user','createdon']


@admin.register(Members)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'country', 'gender','created']
    list_filter = ['country', 'gender']
    search_fields = ('username', 'email', 'firstname', 'lastname')
    date_hierarchy = 'created'


