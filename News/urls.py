from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('', views.news_list, name="newslist"),
    # path('home/' views.)
    path("newsholder", views.main, name="holder"),
    path("publishNews/", views.publish_news, name="publishnews"),
    # path('category_list/', views.category_list, name="categorylist"),
    path('category_featured/<int:pk>/', views.category_detail, name="categoryfeatured"),
    path('newsdetail/<int:pk>/', views.news_detail, name="newsdetail"),
]
