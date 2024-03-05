from django.shortcuts import render, redirect
from .forms import SignUpFrom, JouranlistAcceptance
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import JournalistProfile
from News.models import NewsCategory, News
from django.http import HttpResponse


# Create your views here.

def register(request):
    category = NewsCategory.objects.all()
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
        "category":category,
        "form":signupform
    }

    return render(request, "partials/signup.html", context)    


def signin(request):
    category = NewsCategory.objects.all()
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
    context ={
        "category":category
    }

    return render(request, "partials/signin.html", context)    

@login_required
def signout(request):
    logout(request)
    return redirect("user:signin")

@login_required
def create_profile(request):
    category = NewsCategory.objects.all()
    profile = JournalistProfile.objects.all()
    # category = NewsCategory.objects.all()
    if request.method == "POST":
        profile_picture = request.FILES['profile_image']
        # catagory = request.POST['category']
        bio=request.POST['bio']
        short_intro = request.POST['short_intro']
        CV = request.FILES['upload_cv']
        
        profile = JournalistProfile.objects.create(
            user=request.user,
            profile_image=profile_picture, 
            # category=catagory,
            bio=bio,
            short_intro = short_intro,
            upload_cv = CV
            )
        profile.save()
        return redirect('news:newslist')
        
    context = {
        "category":category,
        'profile':profile
    }

    return render(request, 'partials/userprofileform.html', context)

@user_passes_test(lambda user : user.is_superuser)
def list_of_users(request):
    category = NewsCategory.objects.all()
    users_list = JournalistProfile.objects.all()

    context = {
        "category":category,
        "users_list": users_list
    }
    return render(request, 'partials/userlist.html', context)

@user_passes_test(lambda user: user.is_superuser)
def users_detail(request, pk):
    category = NewsCategory.objects.all()
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
        "category":category
    }

    return render(request, "partials/user_detail.html", context)



# def can_publish_news(request):
#     current_user = request.user
#     current_user_profile = JournalistProfile.objects.get(user=current_user)
#     has_publish_permssion = current_user_profile is not None
    
#     if   has_publish_permssion:
#         context = {
#             "profile": current_user_profile
#         }
#         return render(request, "partials/check_user.html", context)
#     else:
#         return render(request, "partials/404Error.html")
@login_required
def profile(request):
    category = NewsCategory.objects.all()
    # user_information = JournalistProfile.objects.get(journalist_isnull = False)
    current_user = request.user.id
    current_user_profile = JournalistProfile.objects.get(user_id=current_user)
    has_publish_permssion = current_user_profile is not None
    news = News.objects.filter(author_id=current_user) 
    
    if   has_publish_permssion:
         user_profile = current_user_profile
    context = {
        "profile": user_profile,
        "news":news,
        "category":category
        # "info":user_information
         
    }
    return render(request, "partials/profile.html", context)

def profileedit(request, pk):
    category = NewsCategory.objects.all()
    journalist = JournalistProfile.objects.get(id=pk)
    # currentuser = request.user.id
    if request.method == "POST":
        # username = request.POST['username']
        image = request.FILES['profile_image']
        intro = request.POST['short_intro']
        bio = request.POST['bio']
        cv = request.FILES['upload_cv']
        
        journalist.user = request.user
        journalist.profile_image = image
        journalist.short_intro = intro
        journalist.bio = bio
        journalist.upload_cv =  cv


        # currentuser.username = currentuser
        # currentuser.save()

        
        journalist.save()
        return redirect("user:profile")
    

    context = {
        'current_journalist':journalist,
        'category':category
    }
    print(journalist.bio)
    return render(request, 'partials/editprofile.html', context)

    

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