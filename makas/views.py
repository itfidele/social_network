from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import User
# Create your views here.
from .models import Members, Posts, PostImages, Post
from django.core.files.storage import FileSystemStorage
import datetime
from .lib.funcTools import allIneed


def index(request):
    try:
        if request.session['userid']:
            return redirect('dashboard')
    except KeyError:
        return render(request, 'index.html')


def register(request):
    user = User()
    if request.method == "POST":
        data_form = User(request.POST)
        data_form.save()
        return render(request, 'user/register.html', {"forms": user})
    else:
        return render(request, 'user/register.html', {"forms": user})


def dashboard(request):
    try:
        uid = request.session['userid']
        ser = Members.objects.get(pk=uid)
        ser.online = 'yes'
        ser.save()
        allfriends = allIneed(Members).exclude(pk=ser.id)
        allposts = allIneed(Posts)
        context = {
            "myInfo": ser,
            "count_d": allfriends.count,
            "whotofriend": allfriends,
            "posts": allposts,
        }
        return render(request, 'home/dash.html', context)
    except KeyError:
        return redirect('index')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = Members.objects.get(email__exact=username, password__exact=password)
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
            pos.save()
            if request.FILES.getlist('images'):
                myfiles = request.FILES.getlist("images")
                for myfile in myfiles:
                    images = PostImages()
                    p = Post()
                    fs = FileSystemStorage(location='media/post/', base_url='post/')
                    filename = fs.save(myfile.name, myfile)
                    images.attachment = fs.url(filename)
                    images.save()
                    p.postimages = images
                    p.posts = pos
                    p.save()

        return redirect('dashboard')
