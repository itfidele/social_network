from django import template
from ..models import PostLikes,Posts
register=template.Library()

@register.filter
def likes(value):
    post=Posts.objects.get(id=value)
    likes=PostLikes.objects.filter(post=post).count()
    return str(likes)