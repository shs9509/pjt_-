from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    image = models.ImageField(blank=True, null=True)
    title = models.TextField()
    author = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_book')
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    rank = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content