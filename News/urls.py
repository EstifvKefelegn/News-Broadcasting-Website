from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('', views.news_list, name="newslist"),
    # path('home/' views.)
    path("news/news-holder/", views.main, name="holder"),
    path("news/publish-News/", views.publish_news, name="publishnews"),
    # path('category_list/', views.category_list, name="categorylist"),
    path('news/category-detail/<int:pk>/', views.category_detail, name="categorydetail"),
    path('news/<int:pk>/', views.news_detail, name="newsdetail"),
    path("news/edit-news/<int:pk>/", views.edit_news, name="newsedit"),
    path("news/<int:pk>/delete-confirmation/", views.deletenews_confirmation, name="delete_confirmation"),
        
    path("news/<int:pk>/delete-news/", views.deletenews, name="deletenews"),
    path("news/video-list/",views.video_list, name="videolist"),
    path("news/video-list/<int:pk>/",views.video_detail, name="videodetail")
]
