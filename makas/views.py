from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse,Http404
import json
from .forms import User, PostForm, CommentForm
# Create your views here.
from .models import Members, Posts, Comments, PostLikes, Friend
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
import datetime
from rest_framework import generics

# headers:{ 'X-CSRFToken':getcookies('csrftoken') }

from .serializers import MemberSerializer


def album(request):
    try:
        ser = Members.objects.get(pk=request.session['userid'])
        context = {
            'myInfo': ser,
        }
        return render(request, 'home/user-album.html', context)
    except KeyError:
        return redirect('login')


def settings(request):
    try:
        ser = Members.objects.get(pk=request.session['userid'])
        context = {
            'myInfo': ser,
        }
        return render(request, 'home/settings.html', context)
    except KeyError:
        return redirect('login')


def friend_home(request):
    try:
        ser = Members.objects.get(pk=request.session['userid'])
        formpost = PostForm()
        context = {
            'myInfo':ser,
            'formpost':formpost,
            'friends':ser.friends.all()
        }
        return render(request, 'home/home-friends.html', context)
    except KeyError:
        return redirect('login')


class MemberAPI(generics.ListAPIView):
    queryset = Members.objects.all()
    serializer_class = MemberSerializer


class DetailMemberAPI(generics.RetrieveAPIView):
    queryset = Members.objects.all()
    serializer_class = MemberSerializer


def index(request):
    try:
        if request.session['userid']:
            return redirect('dashboard')
    except KeyError:
        return render(request, 'index.html')


def comment(request):
    commentForm = CommentForm()
    comments = Comments()
    if request.POST.get('comment'):
        comment = request.POST.get('comment')
        user = request.session['userid']
        post = request.POST.get('postid')
        comments.comment = comment
        comments.user = user
        comments.post = post
        comments.save()
    else:
        pass


def register(request):
    try:
        if request.session['userid']:
            return redirect('dashboard')
    except KeyError:
        user = User()
        if request.method == "POST":
            data_form = User(request.POST)
            data_form.save()
            return render(request, 'user/register.html', {"forms": user, "msg": "You are registered!"})
        else:
            return render(request, 'user/register.html', {"forms": user, "msg": ""})


def dashboard(request):
    try:
        uid = request.session['userid']
        ser = Members.objects.get(pk=uid)
        ser.online = 'yes'
        ser.save()
        formpost = PostForm()
        likes = PostLikes.objects.all()
        comments = Comments.objects.all()
        allfriends = allIneed(Members).exclude(pk=ser.id)
        allposts = allIneed(Posts).order_by('-createdon')
        posts=list()
        for post in allposts:
            if post.user in ser.friends.all() or post.user==ser:
                posts.append(post)

        page = request.GET.get('page')
        paginator = Paginator(posts, 10)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            "myInfo": ser,
            "count_d": allfriends.count,
            "whotofriend": allfriends,
            "posts": posts,
            'formpost': formpost,
            'comments': comments,
        }
        return render(request, 'home/dash.html', context)
    except KeyError:
        return redirect('index')


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = Members.objects.get(
                email__exact=username, password__exact=password)
            if user:
                request.session['userid'] = user.id
                response = {
                    "message": "Success",
                    "url": "/dashboard"
                }
                return JsonResponse(response)

        except Members.DoesNotExist:
            response = {
                "message": "Invalid",
                "url": ''
            }
            return JsonResponse(response)
    else:
        return index(request)


def logout(request):
    try:
        ser = Members.objects.get(pk=request.session['userid'])
        ser.online = 'no'
        ser.save()
        del request.session['userid']
        return redirect('index')
    except KeyError:
        pass
        return redirect('index')


def post(request):
    if request.method == 'POST':
        if request.POST.get("postcontent") != '':
            postcontent = request.POST.get("postcontent")
            userby = request.session['userid']
            postedby = Members.objects.get(pk=userby)
            pos = Posts()
            pos.postcontent = postcontent
            pos.user = postedby
            pos.attachment = request.FILES.get("attachment")
            pos.save()

            '''
            if request.FILES.getlist('images'):
                myfiles = request.FILES.getlist("images")
                for myfile in myfiles:
                    images = PostImages()
                    p = Post()
                    fs = FileSystemStorage(
                        location='media/post/', base_url='post/')
                    filename = fs.save(myfile.name, myfile)
                    images.attachment = fs.url(filename)
                    images.save()
                    p.postimages = images
                    p.posts = pos
                    p.save()
            '''

        return redirect('dashboard')


def allIneed(ob):
    return ob.objects.all()


@csrf_exempt
def comment(request):
    try:
        if request.POST.get('comment') != '':
            Comment = Comments()
            user = Members.objects.get(id=request.session['userid'])
            comment = request.POST.get('comment')
            post = Posts.objects.get(id=request.POST.get('post_'))

            Comment.comment = comment
            Comment.user = user
            Comment.post = post
            Comment.save()
            context = {
                "username": user.username,
                "msg": "message from webhook",
            }
            return JsonResponse(context, safe=True)
        else:
            return HttpResponse('')
    except KeyError:
        return


def refreshComment(request):
    try:
        Comment = Comments.objects.all()
        post = Posts.objects.get(id=request.GET.get('id'))
        user = Members.objects.get(id=request.session['userid'])
        context = {
            "comments": Comment,
            "post": post,
            "myInfo": user,
        }
        return render(request, 'inc/post-comment.html', context)
    except KeyError:
        return


@csrf_exempt
def like_post(request):
    try:
        Likes = PostLikes()
        post = Posts.objects.get(id=request.POST.get('id'))
        user = Members.objects.get(id=request.session['userid'])
        post.likes.add(user)
        post.save()
        context = {
            "response":True,
        }
        return JsonResponse(context,safe=False)
    except KeyError:
        return


@csrf_exempt
def add_friend(request):
    if request.POST.get('addfriend'):
        id_from = request.POST.get('from')
        id_to = request.POST.get('to')
        friend_from=Members.objects.get(id=id_from)
        friend_to=Members.objects.get(id=id_to)
        addfriend = Friend()
        addfriend.friend_from = friend_from
        addfriend.friend_to = friend_to
        addfriend.save()
        response = {
            "is_added": True,
            "msg": "friend Added",
        }
        return JsonResponse(response, safe=False)
    else:
        raise Http404('Invalid')

@csrf_exempt
def confirm_friend(request):
    if request.POST.get('confirmfriend'):
        conf_id=request.POST.get('confirm_id')
        friend_=Friend.objects.get(id=conf_id)
        ser=Members.objects.get(id=request.session['userid'])
        if friend_.friend_from==ser:
            ser.friends.add(friend_.friend_to)
        else:
            ser.friends.add(friend_.friend_from)
        friend_.delete()
        response={
            "is_confirmed":True,
            "msg":"Friend Confirmed",
        }
        return JsonResponse(response,safe=False)
    else:
        raise Http404('Error')


'''
def handler404(request,*args,**argv):
    response=render_to_response('404.html',{},context_instance=RequestContext(request))
    response.status_code=404
    return response
'''
def handler404(request,exception,template_name='404.html'):
    response=render(None,template_name,{})
    response.status_code=404
    context={
        "url":request.get_full_path
    }
    return render(request,'404.html',context)

'''
def handler500(request,exception,template_name='500.html'):
    response=render(None,template_name,{})
    response.status_code=500
    return response

'''