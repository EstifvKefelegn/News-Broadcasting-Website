from django.urls import path
from . import views

app_name = "user"


urlpatterns = [
    path('auth/signup/', views.register, name="signup"),
    path('auth/signin/', views.signin, name="signin"),
    path('auth/signout/', views.signout, name="signout"),
    path('auth/profileform/', views.create_profile, name="profileform"),
    path('auth/userlist/', views.list_of_users, name="userlist"),
    path('auth/userlist/<int:pk>/', views.users_detail, name="userdetail"),
    # path('', views.can_publish_news),
    path('auth/profile/', views.profile, name="profile"),
    path('auth/profile/edit/<int:pk>/', views.profileedit, name="edit")
    # path('jrprofile/', views.jrprofile, name="jrprofile")
]
