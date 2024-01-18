from django.shortcuts import render, redirect
from .forms import SignUpFrom, JouranlistAcceptance
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import JournalistProfile 
from News.models import NewsCategory
from django.http import HttpResponse


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

@login_required
def signout(request):
    logout(request)
    return redirect("user:signin")

@login_required
def create_profile(request):
    profile = JournalistProfile.objects.all()
    # category = NewsCategory.objects.all()
    if request.method == "POST":
        profile_picture = request.FILES['profile_image']
        # catagory = request.POST['category']
        short_intro = request.POST['short_intro']
        CV = request.FILES['upload_cv']
        
        profile = JournalistProfile.objects.create(
            user=request.user,
            profile_image=profile_picture, 
            # category=catagory,
            short_intro = short_intro,
            upload_cv = CV
            )
        profile.save()
        return redirect('news:newslist')
        
    context = {
        'profile':profile
    }

    return render(request, 'partials/userprofile.html', context)

@user_passes_test(lambda user : user.is_superuser)
def list_of_users(request):
    users_list = JournalistProfile.objects.all()

    context = {
        "users_list": users_list
    }
    return render(request, 'partials/userlist.html', context)

@user_passes_test(lambda user: user.is_superuser)
def users_detail(request, pk):
    user_detail = JournalistProfile.objects.get(id=pk)

    if request.method == "POST":
        form = JouranlistAcceptance(request.POST, instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect("user:userlist")
    else:
        form = JouranlistAcceptance(instance=user_detail)

    context = {
        "detail": user_detail,
        "form": form,
    }

    return render(request, "partials/user_detail.html", context)



# @user_passes_test(lambda user : user.is_superuser)
# def users_detail(request, pk):
#     user_detail = JournalistProfile.objects.get(id=pk)
#     if request.user == "POST":
#         journalist_form = JouranlistAcceptance(request.POST, instance=user_detail)
        
#         if journalist_form.is_valid:
#             journalist_form.save()
#             return redirect("user:userlist")
#     else:
#         journalist_form = JournalistProfile()

        

#     context = {
#         "form":journalist_form,
#         "detail":user_detail
#     }

#     return render(request, "partials/user_detail.html",context)