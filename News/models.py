from django.db import models
from django.contrib.auth.models import User
from userauth.models import JournalistProfile

# Create your models here.

# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=55)
#     bio = models.TextField()

#     def __str__(self) -> str:
#         return self.name

class NewsCategory(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    

class Promotion(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    promo_picture = models.ImageField(upload_to="pictures/", null=True, blank=True)
    promo_videos = models.FileField(upload_to='videos/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title

class News(models.Model):
    author = models.ForeignKey(JournalistProfile, on_delete=models.CASCADE, related_name="journalist")
    # journalist = models.ForeignKey
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    image = models.ImageField(upload_to="pictures/", null=True, blank=True)
    small_image = models.ImageField(upload_to="pictures/", null=True, blank=True)
    small_title =models.CharField(max_length=150, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name="news")
    promotion = models.OneToOneField(Promotion, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"\"{self.title}\" from the \"{self.category}\" category"

    class Meta:
        ordering =["-date_created"]

class Tags(models.Model):
    news = models.ManyToManyField(News)
    tag_name = models.CharField(max_length=100, null=True, blank=True)
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="reviewed_news")
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} reviews for {self.news.title}"

    class Meta:
        ordering = ["created_at"]


class ViewCount(models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=True)

    
class Likes(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    number_of_likes = models.IntegerField()

