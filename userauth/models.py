from django.db import models
from django.contrib.auth.models import User
# from News.models import News
# from News.models import NewsCategory

# Create your models here.

class JournalistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="pictures/")
    # profile_category = models.ForeignKey(NewsCategory, on_delete= models.PROTECT)
    bio = models.CharField(max_length=100)
    short_intro = models.CharField(max_length=500)
    upload_cv = models.FileField(upload_to="Files/")
    can_publish = models.BooleanField(default=False)    

    def __str__(self) -> str:
        return self.user.username
    
