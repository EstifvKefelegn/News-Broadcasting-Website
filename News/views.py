from django.shortcuts import render, get_object_or_404
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
    else:
        form = NewsUploadForm()
    context = {
        "form":form
    }

    return render(request, 'partials/uploadNews.html', context)            


    
