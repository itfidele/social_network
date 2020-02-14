from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import json
from .forms import User, PostForm, CommentForm
# Create your views here.
from .models import Members, Posts, Comments, PostLikes
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

# headers:{ 'X-CSRFToken':getcookies('csrftoken') }


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
        page = request.GET.get('page')
        paginator = Paginator(allposts, 1)
        try:
            allposts = paginator.page(page)
        except PageNotAnInteger:
            allposts = paginator.page(1)
        except EmptyPage:
            allposts = paginator.page(paginator.num_pages)

        context = {
            "myInfo": ser,
            "count_d": allfriends.count,
            "whotofriend": allfriends,
            "posts": allposts,
            'formpost': formpost,
            'comments': comments,
            'likes': likes,
            'thi': 'fiffi',
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
            "msg": "message from webhook"
        }
        return JsonResponse(context, safe=True)
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
def refreshLike(request):
    try:

        if request.POST.get('id'):
            Likes = PostLikes()
            post = Posts.objects.get(id=request.POST.get('id'))
            user = Members.objects.get(id=request.session['userid'])
            Likes.user = user
            Likes.post = post
            Likes.like = 1
            Likes.save()
        else:
            post = Posts.objects.get(id=request.GET.get('id'))
        context = {
            "id": post.id,
        }
        return render(request, 'inc/post_likes.html', context)
    except KeyError:
        return
