from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import NewsUploadForm
from .models import News, NewsCategory, Review
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
    
def video_list(request):
    category = NewsCategory.objects.all()
    video_news = News.objects.all()
    
    if request.method == "POST":
        search_input = request.POST['search-input']
        video_news = News.objects.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))


    context = {
        "category":category,
        "video_news":video_news,

    }
    return render(request, 'partials/video_news.html', context)

def video_detail(request,pk):
    category = NewsCategory.objects.all()
    video_detail = News.objects.get(id=pk)

    context = {
        "category":category,
        "video_detail":video_detail
    }
    return render(request, "partials/video_detail.html", context)
def category_detail(request, pk):
    category = NewsCategory.objects.all()
    category_detail = NewsCategory.objects.get(id=pk)
    news_article = News.objects.filter(category=category_detail)
    category_image = category_detail.news.filter(image__isnull=False)

    context = {
        "category":category,
        "category_detail": category_detail,
        "category_image":category_image,
        "news_article":news_article
    }
    return render(request, 'partials/category_detail.html', context)

@login_required
def publish_news(request):
    category = NewsCategory.objects.all()
    if request.method == "POST":
        form = NewsUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("news:newslist")
        else:
            print(form.errors)
    else:
        form = NewsUploadForm()
    context = {
        "category":category,
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

        # bottoms
        bottom_main_first = list_of_news[5]
        bottom_main_second = list_of_news[6]
        bottom_left_first = list_of_news[7]
        bottom_left_second = list_of_news[8]
        bottom_left_third = list_of_news[9]
        bottom_left_forth = list_of_news[10]
        bottom_left_fifth =list_of_news[11]
        bottom_left_six = list_of_news[12]
        bottom_left_seven =list_of_news[13]
        bottom_left_eight = list_of_news[14]

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
        "bottom_main_first":bottom_main_first,
        'bottom_main_second':bottom_main_second,
        "bottom_left_first":bottom_left_first,
        "bottom_left_second":bottom_left_second,
        "bottom_left_third":bottom_left_third,
        "bottom_left_fourth":bottom_left_forth,
        "bottom_left_fifth":bottom_left_fifth,
        "bottom_left_six":bottom_left_six,
        "bottom_left_seven":bottom_left_seven,
        "bottom_left_eight":bottom_left_eight, 
        # "profile": current_user 
    }
    
    return render(request, "base/home.html", context)


def news_detail(request, pk):
    category = NewsCategory.objects.all()
    detail_news = News.objects.get(id=pk)
    recent_posts = News.objects.filter(category=detail_news.category)[:4]
    #This line manages the user review
    user_review = Review.objects.filter(news=detail_news)

    description = detail_news.description
    part_length = len(description) // 4
    first_part = description[:part_length]
    second_part = description[part_length:2*part_length]
    third_part = description[part_length:3*part_length:]
    fourth_part = description[3*part_length:]
    if request.method == "POST":
        comment_body = request.POST['comment_body']
        
        # Create an instance of Review
        new_user_review = Review(user=request.user, news=detail_news, review_text=comment_body)
        
        # Save the instance
        new_user_review.save()

        return redirect("news:newslist")

    promotion = detail_news.promotion.title if detail_news.promotion else None
    print(promotion)
    context = {
        "category":category,
        "detail": detail_news,
        "first_body_part": first_part,
        "second_body_part": second_part,
        "third_body_part": third_part,
        "fourth_part": fourth_part,
        "review":user_review,
        "recent_posts": recent_posts
    }

    return render(request, "partials/newsdetail.html", context)




def edit_news(request, pk):
    category = NewsCategory.objects.all()
    news_instance = News.objects.get(pk=pk)

    if request.method == 'POST':
        form = NewsUploadForm(request.POST, request.FILES, instance=news_instance)
        if form.is_valid():
            form.save()
            return redirect("user:profile")  # Replace 'success_page' with the actual URL name for the success page
    else:
        form = NewsUploadForm(instance=news_instance)

    context = {'form': form, 'news_instance': news_instance, "category":category} 

    return render(request, 'partials/editnews.html', context)

# def edit_news(request, pk):
   
#     book_detail = News.objects.get(id=pk)
#     if request.method == "POST":
#         edit_news = NewsUploadForm(request.POST, request.FILES,instance=book_detail)
#         if edit_news.is_valid():
#             edit_news.save()
#             return redirect("user:profile")
#     context = {
        
#         "detail": book_detail,
#         "form":NewsUploadForm(instance=book_detail)
#     }    
    
#     return render(request, 'partials/editnews.html', context)

def deletenews_confirmation(request, pk):
    category = NewsCategory.objects.all()
    news_instance = News.objects.get(id=pk)

    context = {
        "category":category,
        "news":news_instance,
    } 
    return render(request, 'partials/delete_confirmation.html', context)

def deletenews(request, pk):
    
    news = News.objects.get(id=pk)
    # if request.method == "POST":
    news.delete()
    return redirect("user:profile")
    # return redirect("user:profile")

def comment_display(request):
    review = Review.objects.all()

