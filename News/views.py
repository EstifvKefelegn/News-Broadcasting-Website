from django.shortcuts import render
from .form import NewsUploadForm
from .models import News

# Create your views here.
def main(request):
    return render(request, 'base/index.html')

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

