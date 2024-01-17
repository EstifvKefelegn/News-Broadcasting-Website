from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .form import NewsUploadForm
from .models import News, NewsCategory

# Create your views here.
def main(request):
    catgeory = NewsCategory.objects.all()


    # videos = category_detail.news.filter(image__isnull = False).order_by('-date_created')[:4]

    context = {
        'category':catgeory,
    }
    return render(request, 'base/index.html', context)
    



def category_detail(request, pk):
    category_detail = NewsCategory.objects.get(id=pk)
    category_image = category_detail.news.filter(image__isnull=False)

    context = {
        "category_detail": category_detail,
        "category_image":category_image 
    }
    return render(request, 'partials/category_detail.html', context)

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
    news = News.objects.all()
    list_of_news =[] 
    
    for new in news:
        list_of_news.append(new)
    try:
        left_main_news = list_of_news[0]
        top_main_news = list_of_news[1]
        bottom_main_news1 = list_of_news[2]
        bottom_main_news2 = list_of_news[3]
        right_main_news = list_of_news[4]
        
    except FileNotFoundError:
        print("file not found")    
    print(left_main_news.category)
    
    context = {
        "news":new,
        "left_main_news":left_main_news,
        "top_main_news":top_main_news,
        "bottom_main_news1":bottom_main_news1,
        "bottom_main_news2":bottom_main_news2,
        "right_main_news":right_main_news
    }
    
    return render(request, "base/home.html", context)


def news_detail(request, pk):
    detail_news = News.objects.get(id=pk)
    # print(detail_news)

    context = {
        "detail": detail_news
    }

    return render(request, "partials/newsdetail.html", context)



