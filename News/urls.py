from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('news/', views.news_list, name="newslist"),
    # path('home/' views.)
    path("news/newsholder/", views.main, name="holder"),
    path("news/publishNews/", views.publish_news, name="publishnews"),
    # path('category_list/', views.category_list, name="categorylist"),
    path('news/category_featured/<int:pk>/', views.category_detail, name="categoryfeatured"),
    path('news/<int:pk>/', views.news_detail, name="newsdetail"),
]
