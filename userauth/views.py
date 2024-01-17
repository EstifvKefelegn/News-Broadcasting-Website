from django.shortcuts import render, redirect
from .forms import SignUpFrom
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    signupform = SignUpFrom()
    if request.method == "POST":
        signupform = SignUpFrom(request.POST)
        if signupform.is_valid():
            form = signupform.save()
            messages.success(request, f"You are successfuly registered ")
            
            return redirect("news:newslist")
    elif request.user.is_authenticated:
        messages.warning(request, f"You are already registered we are processign your CV")
    else:
        signupform = SignUpFrom()
    
    context = {
        "form":signupform
    }

    return render(request, "partials/signup.html", context)    


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully logged in.')
            return redirect('news:newslist')
        else:
            messages.warning(request, 'Username or password is incorrect.')

    # return render(request, 'users/signin.html')

    return render(request, "partials/signin.html")    

def signout(request):
    logout(request)
    return redirect("user:signin")