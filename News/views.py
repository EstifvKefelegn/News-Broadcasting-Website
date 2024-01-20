from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import NewsUploadForm
from .models import News, NewsCategory
from userauth.models import JournalistProfile

# Create your views here.
def main(request):
    category = NewsCategory.objects.all()
    user = request.user
  

    context = {
        'category':category,
        # 'profile': current_user if has_journalist_profile else None,
        'user': user
    }

    # if has_journalist_profile:
    #     context['profile'] = current_user
    #     print(current_user.can_publish)
    # print(context['profile'].can_publish)     
    
    return render(request, 'base/index.html', context)
    



def category_detail(request, pk):
    category_detail = NewsCategory.objects.get(id=pk)
    category_image = category_detail.news.filter(image__isnull=False)

    context = {
        "category_detail": category_detail,
        "category_image":category_image 
    }
    return render(request, 'partials/category_detail.html', context)

@login_required
def publish_news(request):
    if request.method == "POST":
        form = NewsUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("news:newslist")
    else:
        form = NewsUploadForm()
    context = {
        "form":form
    }
    
    return render(request, 'partials/uploadNews.html', context)            


def news_list(request):
    category = NewsCategory.objects.all() 
    news = News.objects.all()
    list_of_news =[] 

    user_id = request.user.id
    current_user = JournalistProfile.objects.filter(user_id=user_id).first()
    has_journalist_profile = current_user is not None
    


    for new in news:
        list_of_news.append(new)
    if list_of_news:
        left_main_news = list_of_news[0]
        top_main_news = list_of_news[1]
        bottom_main_news1 = list_of_news[2]
        bottom_main_news2 = list_of_news[3]
        right_main_news = list_of_news[4]
    elif not list_of_news and has_journalist_profile == True:    
            return render(request, "base/index.html")    
    else:
        messages.warning(request, "File not found")    
        return render(request, 'partials/404Error.html')

    context = {
        'category':category,
        "news":news,
        "left_main_news":left_main_news,
        "top_main_news":top_main_news,
        "bottom_main_news1":bottom_main_news1,
        "bottom_main_news2":bottom_main_news2,
        "right_main_news":right_main_news,
        

        # "profile": current_user 
    }
    
    # if has_journalist_profile:
    #     context['profile'] = current_user
    #     print(current_user.can_publish)
    return render(request, "base/home.html", context)


def news_detail(request, pk):
    detail_news = News.objects.get(id=pk)
    # print(detail_news)

    context = {
        "detail": detail_news
    }

    return render(request, "partials/newsdetail.html", context)

def edit_news(request, pk):
   
    book_detail = News.objects.get(id=pk)
    if request.method == "POST":
        edit_news = NewsUploadForm(request.POST, request.FILES,instance=book_detail)
        if edit_news.is_valid():
            edit_news.save()
            return redirect("user:profile")
        else:
            print(edit_news.errors)
    context = {
        
        "detail": book_detail,
        "form":NewsUploadForm(instance=book_detail)
    }    
    
    return render(request, 'partials/editnews.html', context)

def deletenews_confirmation(request, pk):
    news_instance = News.objects.get(id=pk)

    context = {
        "news":news_instance
    } 
    return render(request, 'partials/delete_confirmation.html', context)

def deletenews(request, pk):
    news = News.objects.get(id=pk)
    # if request.method == "POST":
    news.delete()
    return redirect("user:profile")
    # return redirect("user:profile")

# def deletenews(request, pk):
#     news = News.objects.get(id=pk)
#     news.delete()
    
#     context = {
#         "news":news
#     }

#     return render(request, "partials/delete.html", context)


# def can_publish_news(request):

#         return render(request, "/check_user.html", context)
    
#     return render(request, "partials/404Error.html")