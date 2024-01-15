from django.db import models
# from django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    bio = models.TextField()

class NewsCategory(models.Model):
    category_name = models.CharField(max_length=100)

class Promotion(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    promo_picture = models.ImageField(upload_to="pictures/", null=True, blank=True)
    promo_videos = models.FileField(upload_to='videos/', null=True, blank=True)

class News(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    image = models.ImageField(upload_to="pictures/", null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    promotion = models.ManyToManyField(Promotion)


class Tags(models.Model):
    news = models.ManyToManyField(News)
    tag_name = models.CharField(max_length=100, null=True, blank=True)
    

class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} reviews for {self.news.title}"
    

class ViewCount(models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=True)

    