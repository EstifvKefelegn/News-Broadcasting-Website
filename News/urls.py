from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.main, name="main"),
    path("publishNews/", views.publish_news, name="publishnews")
]
