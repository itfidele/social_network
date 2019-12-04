from django.shortcuts import render
from .forms import User
# Create your views here.
from .models import Users

def index(request):
    users=[
        {
            "name":"fidele",
        },
        {
            "name":"Fidele",
        }
    ]
    context={
        "users":users,
    }

    return render(request,'index.html',context=context)


def register(request):
    if request.method=="POST":
        fname=request.POST.get("firstname")
        return render(request,'user/register.html',{"name":fname})
    else:
        one=Users(pk=1)
        user=User()
        return render(request,'user/register.html',{"forms":user})

def dashboard(request):
    return render(request,'home/dash.html')