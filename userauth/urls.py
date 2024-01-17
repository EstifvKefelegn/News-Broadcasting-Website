from django.urls import path
from . import views

app_name = "user"


urlpatterns = [
    path('signup/', views.register, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout")
]
