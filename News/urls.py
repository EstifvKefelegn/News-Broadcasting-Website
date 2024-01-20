from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('news/', views.news_list, name="newslist"),
    # path('home/' views.)
    path("news/news-holder/", views.main, name="holder"),
    path("news/publish-News/", views.publish_news, name="publishnews"),
    # path('category_list/', views.category_list, name="categorylist"),
    path('news/category-featured/<int:pk>/', views.category_detail, name="categoryfeatured"),
    path('news/<int:pk>/', views.news_detail, name="newsdetail"),
    path("news/edit-news/<int:pk>/", views.edit_news, name="newsedit"),
    path("news/<int:pk>/delete-confirmation/", views.deletenews_confirmation, name="delete_confirmation"),
        
    path("news/<int:pk>/delete-news/", views.deletenews, name="deletenews")
]
