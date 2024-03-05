from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q, Count, Prefetch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .form import NewsUploadForm
from .models import News, NewsCategory, Review, ViewCount, Promotion
from userauth.models import JournalistProfile
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext



# # Create your views here.
def translate(language):
    cur_language = activate(language)
    try:
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text


def main(request):
    category = NewsCategory.objects.prefetch_related('news').all()
    print(category)
    user = request.user
    if request.method == 'POST':
        selected_language = request.POST.get('language', 'en')
        trans = translate(language=selected_language)
    else:
        # If the form is not submitted, use the default language
        trans = translate(language="en")

    # return render(request, "home.html", {"trans": trans})       

    context = {
        'category':category,
        # 'profile': current_user if has_journalist_profile else None,
        'user': user,
        "trans": trans
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
    current_journalist = video_detail.author
    last_posted_news = News.objects.filter(author=current_journalist).order_by('-date_created')[:2]
    recent_posts = News.objects.filter(category=video_detail.category)[:4]
    current_category_news = News.objects.filter(category=video_detail.category).order_by('-date_created')[:2]
    #This line manages the user review
    user_review = Review.objects.filter(news=video_detail)
    if request.method == "POST":
        comment_body = request.POST['comment_body']
        
        # Create an instance of Review
        new_user_review = Review(user=request.user, news=video_detail, review_text=comment_body)
        
        # Save the instance
        new_user_review.save()

        return redirect("news:newslist")


    context = {
        "category":category,
        "video_detail":video_detail,
        "review":user_review,
        "recent_posts": recent_posts,
        "last_posted_news":last_posted_news,
        "current_journalist":current_journalist,
        "current_category":current_category_news
    }
    return render(request, "partials/video_detail.html", context)
def category_detail(request, pk):
    category = NewsCategory.objects.all()
    category_detail = NewsCategory.objects.prefetch_related('news').get(id=pk)
    news_article = News.objects.filter(category=category_detail).select_related('author')

    # Use prefetch_related to fetch related images for the category in a single query
    category_image = NewsCategory.objects.filter(id=pk).prefetch_related(
        Prefetch('news', queryset=News.objects.filter(image__isnull=False))
    ).first()
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
    category_id = int(request.POST['news-category'])
    selected_category = NewsCategory.objects.get(id=category_id)
    journalist_profile = JournalistProfile.objects.get(user=request.user)
    if request.method == "POST":
        news = News.objects.create(
          author=journalist_profile,
          title = request.POST['news-title'],
          description = request.POST['news-desc'],
          video = request.FILES['news-video'],
          image = request.FILES['news-image'],
          second_image= request.FILES['news-second-image'],
          small_image = request.FILES['news-small-image'],
          source = request.POST['source'],
          category = selected_category
         )
        return redirect('news:newslist') 
    
    context = {
        "category": category,
        # "form": form
    }

    return render(request, 'partials/uploadNews.html', context)
def news_list(request):
    # Fetch NewsCategory objects only once
    category = NewsCategory.objects.prefetch_related('news').all() 

    news = News.objects.select_related('category').all()
    journalist_requests = JournalistProfile.objects.filter(can_publish=False).count() 
    left_news = News.objects.all()[5:]
    list_of_news = [] 

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
    elif not list_of_news and has_journalist_profile:
        return render(request, "base/index.html")
    else:
        messages.warning(request, "File not found")
        return render(request, 'partials/404Error.html')

    context = {
        'category': category,
        "news": news,
        "left_main_news": left_main_news,
        "top_main_news": top_main_news,
        "bottom_main_news1": bottom_main_news1,
        "bottom_main_news2": bottom_main_news2,
        "right_main_news": right_main_news,
        "left_news": left_news,
        "journalist_requests": journalist_requests
    }
    
    return render(request, "base/home.html", context)


def news_detail(request, pk):
    current_user = request.user 
    category = NewsCategory.objects.all()
    detail_news = News.objects.get(id=pk)
    # promotion =get_object_or_404(Promotion, news=detail_news)
    view_count, created = ViewCount.objects.get_or_create(news=detail_news)
    current_journalist = detail_news.author
    last_posted_news = News.objects.filter(author=current_journalist).order_by('-date_created')[:2]
    recent_posts = News.objects.filter(category=detail_news.category)[:4]
    current_category_news = News.objects.filter(category=detail_news.category).order_by('-date_created')[:2]
    
    try:
        # Attempt to get the related Promotion
        promotion = Promotion.objects.get(news=detail_news)
    except ObjectDoesNotExist:
        # If the related Promotion does not exist, set promotion to None
        promotion = None



    if created:
        # If the ViewCount object was just created, increment the count
        view_count.count += 1
    else:
        # If the ViewCount object already existed, update the count
        view_count.count += 1

    # Save the updated view count
    view_count.save()
        
    #This line manages the user review
    user_review = Review.objects.filter(news=detail_news)
    # detail_news.view_count += 1
    # detail_news.save()
    
    description = detail_news.description
    part_length = len(description) // 4
    first_part = description[:part_length]
    second_part = description[part_length:2*part_length]
    third_part = description[part_length:3*part_length:]
    fourth_part = description[3*part_length:]

    if request.method == "POST":
        comment_body = request.POST['comment_body']
        
        # Create an instance of Review
        new_user_review = Review(user=current_user, news=detail_news, review_text=comment_body)
        
        # Save the instance
        new_user_review.save()

        return redirect("news:newslist")


    
    context = {
        "category":category,
        "detail": detail_news,
        "first_body_part": first_part,
        "second_body_part": second_part,
        "third_body_part": third_part,
        "fourth_part": fourth_part,
        "review":user_review,
        "recent_posts": recent_posts,
        "last_posted_news":last_posted_news,
        "current_journalist":current_journalist,
        "current_category":current_category_news,
        "view_count":view_count.count,
        'promotion':promotion,
        "current_user":current_user
    }

    return render(request, "partials/newsdetail.html", context)

# def comments(request, pk):
#     detail_news = News.objects.get(id=pk)
#     current_journalist = detail_news.author
#     last_posted_news = News.objects.filter(author=current_journalist).order_by('-date_created')[:2]
#     user_review = Review.objects.filter(news=detail_news)
    
#     if request.method == "POST":
#         comment_body = request.POST['comment_body']
        
#         # Create an instance of Review
#         new_user_review = Review(user=request.user, news=detail_news, review_text=comment_body)
        
#         # Save the instance
#         new_user_review.save()

#         return redirect("news:newslist")
#     context = {
#         "detail": detail_news,
#         "review":user_review,
#         "last_posted_news":last_posted_news,
#         "current_journalist":current_journalist,
     
#     }
#     return render(request, "partials/comments.html", context)


def edit_news(request, pk):
    category = NewsCategory.objects.all()
    current_news = News.objects.get(id=pk)
    journalist_profile = JournalistProfile.objects.get(user=request.user)

    if request.method == "POST":
        category_id = int(request.POST['news-category'])
        selected_category = NewsCategory.objects.get(id=category_id)
        News.objects.create(
          author= journalist_profile,
          title = request.POST['news-title'],
          small_title = request.POST['news-small-title'],
          description = request.POST['news-desc'],
          video = request.FILES['news-video'],
          image = request.FILES['news-image'],
          second_image= request.FILES['news-second-image'],
          small_image = request.FILES['news-small-image'],
          source = request.POST['source'],
          category = selected_category
         )
        return redirect('news:newslist')
    context = {"category":category, "current_news":current_news} 

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

def add_promotion(request):
    user_news = request.user.journalistprofile
    current_news = News.objects.filter(author=user_news)
    if request.method == 'POST':
        title =request.POST['promo-title']
        picture = request.FILES['promo-picture']
        video = request.FILES['promo-video']
        news_id = request.POST['promo-news']
        # return redirect("news:newslist")


        new_promotion = Promotion.objects.create(
            title=title,
            promo_picture=picture,
            promo_videos=video,
        )    

        if news_id:
            news = News.objects.get(pk=news_id)
            new_promotion.news = news
        new_promotion.save()
        return redirect("news:newslist")


  
    context = {
        "user_posted_news": current_news

    }    
    return render(request, "partials/promotion.html", context)

def edit_promotion(request, pk):
    promotionform = Promotion.objects.get(id=pk)
    
    if request.method == "POST":
        promo_title = request.POST['promo-title']
        promo_picture = request.FILES.get('promo-picture')
        promo_video = request.FILES.get('promo-video')

        promotionform.title = promo_title   
        if promo_picture:
            promotionform.promo_picture = promo_picture
        if promo_video:
            promotionform.promo_videos = promo_video

        promotionform.save()
        return redirect("news:newslist")
    context = {
        "promotionform":promotionform
    }

    return render(request, 'partials/editpromotion.html', context)        



# def comment_display(request):
#     review = Review.objects.all()


