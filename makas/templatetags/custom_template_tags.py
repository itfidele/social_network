from django import template
from ..models import PostLikes, Posts, Friend
from django.db.models import Q
register = template.Library()


@register.filter
def likes(value):
    post = Posts.objects.get(id=value)
    likes = PostLikes.objects.filter(post=post).count()
    return str(likes)


@register.simple_tag
def is_not_friend(f_rom, t_o):
    friend = Friend.objects.filter(Q(friend_from=f_rom) & Q(friend_to=t_o) | Q(
        friend_to=f_rom) & Q(friend_from=t_o)).count()
    if friend>0:
        return False
    else:
        return True