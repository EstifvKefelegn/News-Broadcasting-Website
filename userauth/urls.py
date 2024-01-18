from django.urls import path
from . import views

app_name = "user"


urlpatterns = [
    path('auth/signup/', views.register, name="signup"),
    path('auth/signin/', views.signin, name="signin"),
    path('auth/signout/', views.signout, name="signout"),
    path('auth/profile/', views.create_profile, name="profile"),
    path('auth/userlist/', views.list_of_users, name="userlist"),
    path('auth/userlist/<int:pk>/', views.users_detail, name="userdetail")
    # path('jrprofile/', views.jrprofile, name="jrprofile")
]
